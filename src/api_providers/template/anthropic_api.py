from api_defines.bee.models.anthropic_args import AnthropicArgs
from api_defines.bee.models.anthropic_result import (
    AnthropicResult as BeeAnthropicResult,
    AnthropicStreamChunkResult as BeeAnthropicStreamChunkResult,
)
from services import env_service
from services.log_service import logger
import random

urls=[]


async def set_urls():
    global urls
    if len(urls) > 0:
        return

    env_urls=env_service.get_chat_url()
    urls=env_urls.split(";")
    logger.info(f"anthropic urls: {urls}")


async def get_url():
    url=random.choice(urls)
    return url


async def init():
    """
    初始化函数
    """
    await set_urls()


async def get_request_url(args:AnthropicArgs):
    """
    获取请求 URL 函数
    """
    global urls
    if len(urls) == 0:
        await set_urls()

    if len(urls) == 0:
        raise ValueError("anthropic urls is empty")

    url=await get_url()
    return url


async def get_request_headers(token: str):
    """
    获取请求头函数

    Anthropic 使用 x-api-key 认证，并需要 anthropic-version 版本头。
    """
    # 认证密钥
    auth_key=None
    if token is None:
        auth_key=env_service.get_auth_key()
    else:
        auth_key=token

    headers = {
        "Content-Type": "application/json",
        "x-api-key": f"{auth_key}",
        "anthropic-version": "2023-06-01",
    }
    return headers


async def get_request_args(args:AnthropicArgs)->dict:
    """Anthropic Messages API 参数转为当前对接平台的参数格式

    Args:
        args (AnthropicArgs): 请求参数对象

    Returns:
        dict: 当前对接平台的参数格式的字典对象
    """

    """
    Anthropic Messages API 参数完整格式参考:
    {
        "model": "claude-opus-5-5",
        "max_tokens": 4096,
        "system": "你是一位助手",
        "messages": [
            {
                "role": "user",
                "content": "你好"
            }
        ]
    }
    """
    # 组装为当前对接平台的参数格式
    args_json=args.model_dump(exclude_none=True)
    # args_dict={
    #     "model": args_json["model"],
    #     "max_tokens": args_json["max_tokens"],
    #     "system": args_json.get("system"),
    #     "messages": args_json["messages"],
    #     "stream": args_json.get("stream"),
    #     "temperature": args_json.get("temperature"),
    #     "top_p": args_json.get("top_p"),
    #     "tools": args_json.get("tools"),
    # }
    args_dict=args_json
    return args_dict


async def get_request_result(result:dict)->BeeAnthropicResult:
    """获取请求结果，转换为 Anthropic Messages API 格式

    Args:
        result (dict): 请求参数对象

    Returns:
        BeeAnthropicResult: 返回的 Anthropic Messages API 格式的结果对象
    """

    """
    Anthropic Messages API 返回结果完整格式参考:
    {
        "id": "msg_xxx",
        "type": "message",
        "role": "assistant",
        "model": "claude-opus-5-5",
        "stop_reason": "end_turn",
        "content": [
            {
                "type": "text",
                "text": "你好，有什么可以帮你？"
            }
        ],
        "usage": {
            "input_tokens": 10,
            "output_tokens": 20
        }
    }
    """

    # result_dict = {
    #     "id": result["id"],
    #     "type": result["type"],
    #     "role": result["role"],
    #     "model": result["model"],
    #     "stop_reason": result["stop_reason"],
    #     "content": result["content"],
    #     "usage": result["usage"]
    # }
    result_dict=result
    result_obj = BeeAnthropicResult(**result_dict)
    return result_obj


async def get_request_stream_chunk_result(result:dict)->BeeAnthropicStreamChunkResult:
    """获取流式请求块结果，转换为 Anthropic Messages API 格式

    Args:
        result (dict): 单个 SSE 事件

    Returns:
        BeeAnthropicStreamChunkResult: 返回的 Anthropic Messages API 格式的流式结果对象
    """

    """
    Anthropic 流式事件完整格式参考:
    {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"你好"}}
    {"type":"message_delta","delta":{"stop_reason":"end_turn"},"usage":{"output_tokens":20}}
    {"type":"message_stop"}
    """
    result_dict=result
    result_obj = BeeAnthropicStreamChunkResult(**result_dict)
    return result_obj
