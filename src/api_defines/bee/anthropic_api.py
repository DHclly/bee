
from fastapi.responses import StreamingResponse
from httpx_sse import aconnect_sse

from services import env_service
from services.http_service import http_clients
from services.log_service import logger
from services.sse_service import get_sse_message

from .models.anthropic_args import AnthropicArgs
from .models.error_result import APIErrorResult

import random

# Anthropic Messages API 版本头
ANTHROPIC_VERSION = "2023-06-01"

urls = []


async def _set_urls():
    global urls
    if len(urls) > 0:
        return

    env_urls = env_service.get_chat_url()
    urls = env_urls.split(";")
    logger.info(f"anthropic urls: {urls}")


async def _get_request_url() -> str:
    global urls
    if len(urls) == 0:
        await _set_urls()

    if len(urls) == 0:
        raise ValueError("anthropic urls is empty")

    return random.choice(urls)


def _get_request_headers(token: str) -> dict:
    # Anthropic 使用 x-api-key 认证，并需要 anthropic-version 版本头
    auth_key = env_service.get_auth_key() if token is None else token
    return {
        "Content-Type": "application/json",
        "x-api-key": f"{auth_key}",
        "anthropic-version": ANTHROPIC_VERSION,
    }


def _get_request_args(args: AnthropicArgs) -> dict:
    # 请求体直接使用 Anthropic 原生参数，仅剔除未传的可选字段
    return args.model_dump(exclude_none=True)


async def anthropic_messages(args: AnthropicArgs, token: str) -> dict | StreamingResponse | APIErrorResult:
    """
    转发 Anthropic Messages API 请求。

    - 非流式：直接返回上游 JSON
    - 流式：把上游 SSE 事件原样透传为 text/event-stream
    """
    response_error_text = ""
    try:
        request_url = await _get_request_url()
        request_headers = _get_request_headers(token)
        request_args = _get_request_args(args)
        client = http_clients.chat_client

        logger.info(f"发起 Anthropic 消息请求,地址:{request_url}\n")
        logger.debug(f"请求头参数：{request_headers}\n")
        logger.debug(f"请求参数：{request_args}\n")

        if args.stream:
            async def stream_generator():
                async with aconnect_sse(
                    client,
                    "POST",
                    url=request_url,
                    headers=request_headers,
                    json=request_args,
                ) as event_source:
                    if event_source.response.status_code != 200:
                        msg = (await event_source.response.aread()).decode(encoding="utf-8", errors="ignore")
                        logger.info("请求失败，错误信息：" + msg)
                        api_error_json = APIErrorResult(code="000", message=msg).model_dump_json()
                        yield get_sse_message(api_error_json)
                    else:
                        async for line in event_source.aiter_sse():
                            if line.data is None:
                                continue
                            if line.data == "[DONE]":
                                yield get_sse_message(line.data)
                                logger.debug("停止流式输出\n")
                                continue
                            logger.debug(f"原始返回参数：{line.data}\n")
                            # Anthropic 事件带 event 名（如 content_block_delta），需保留 event 行
                            yield f"event: {line.event}\ndata: {line.data}\n\n"

            return StreamingResponse(
                content=stream_generator(),
                status_code=200,
                headers={"proxy-server": "bee"},
                media_type="text/event-stream"
            )

        response = await client.post(
            url=request_url,
            headers=request_headers,
            json=request_args)
        response_error_text = ",响应信息：" + response.text

        response.raise_for_status()
        result_data = response.json()
        logger.debug(f"原始返回参数：{result_data}\n")
        logger.info("Anthropic 消息请求成功")
        return result_data
    except Exception as e:
        error_text = f"Anthropic 消息请求发生错误，异常类型：{str(type(e))},异常信息：{e} {response_error_text}"
        logger.error(error_text)
        return APIErrorResult(message=error_text)
