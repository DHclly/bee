
from fastapi.responses import StreamingResponse
from httpx_sse import aconnect_sse

from services.http_service import http_clients
from services.log_service import logger
from services.module_load_service import load_anthropic_api
from services.sse_service import get_sse_message

from .models.anthropic_args import AnthropicArgs
from .models.anthropic_result import AnthropicResult as BeeAnthropicResult
from .models.error_result import APIErrorResult
import asyncio

anthropic_api=None
anthropic_api_initialized = False
anthropic_api_lock = asyncio.Lock()

async def anthropic_messages(args:AnthropicArgs,token: str)->BeeAnthropicResult | StreamingResponse | APIErrorResult:
    response_error_text=""
    global anthropic_api, anthropic_api_initialized
    try:
        if not anthropic_api_initialized:
            async with anthropic_api_lock:
                if not anthropic_api_initialized:
                    anthropic_api = load_anthropic_api()
                    await anthropic_api.init() # type: ignore
                    anthropic_api_initialized=True

        request_url=await anthropic_api.get_request_url(args) # type: ignore
        request_headers =await anthropic_api.get_request_headers(token) # type: ignore
        request_args =await anthropic_api.get_request_args(pre_process_args(args)) # type: ignore
        client=http_clients.chat_client

        logger.info(f"发起 Anthropic 消息请求,地址:{request_url}\n")
        logger.debug(f"请求头参数：{request_headers}\n")
        logger.debug(f"原始请求参数：{args.model_dump_json()}\n")
        logger.debug(f"修改后请求参数：{request_args}\n")

        if args.stream:
            # 定义流式生成器
            async def stream_generator():
                async with aconnect_sse(
                    client,
                    "POST",
                    url=request_url,
                    headers=request_headers,
                    json=request_args,
                ) as event_source:
                    if event_source.response.status_code != 200:
                        msg=(await event_source.response.aread()).decode(encoding="utf-8",errors="ignore")
                        logger.info("请求失败，错误信息："+msg)
                        api_error_json = APIErrorResult(code="000",message=msg).model_dump_json()
                        error_line=get_sse_message(api_error_json)
                        yield error_line
                    else:
                        async for line in event_source.aiter_sse():
                            if line.data is None:
                                continue

                            # [DONE]
                            if line.data=="[DONE]":
                                yield get_sse_message(line.data)
                                logger.debug("停止流式输出\n")
                                continue

                            line_data=line.json()
                            logger.debug(f"原始返回参数：{line_data}\n")
                            new_line_data=await anthropic_api.get_request_stream_chunk_result(line_data) # type: ignore
                            new_line_data_json=new_line_data.model_dump_json()
                            logger.debug(f"修改后返回参数：{new_line_data_json}\n")
                            # Anthropic SSE 以 event 名区分事件类型，需保留
                            new_line=get_sse_message(new_line_data_json,event=new_line_data.type)
                            yield new_line

            return StreamingResponse(
                content=stream_generator(),
                status_code=200,
                headers={
                    "proxy-server":"bee"
                    },
                media_type="text/event-stream"
            )
        else:
            response = await client.post(
                url=request_url,
                headers=request_headers,
                json=request_args)
            response_error_text=",响应信息："+response.text

            response.raise_for_status()
            result_data = response.json()
            logger.debug(f"原始返回参数：{result_data}\n")
            result =await anthropic_api.get_request_result(result_data) # type: ignore
            logger.debug(f"修改后返回参数：{result.model_dump_json()}\n")
            logger.info("Anthropic 消息请求成功")
            return result
    except Exception as e:
        error_text=f"Anthropic 消息请求发生错误，异常类型：{str(type(e))},异常信息：{e} {response_error_text}"
        logger.error(error_text)
        return APIErrorResult(message=error_text)


def pre_process_args(args:AnthropicArgs)->AnthropicArgs:
    return args
