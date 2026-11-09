import json
import random
import time

from api_defines.bee.models.chat_args import ChatArgs as BeeChatArgs
from api_defines.bee.models.chat_result import ChatResult as BeeChatResult
from api_defines.bee.models.chat_result import (
    ChatStreamChunkResult as BeeChatStreamChunkResult,
    ChatChoiceModel,
    ChatStreamChoiceModel,
    ChatChoiceDeltaModel,
    ChatUsageModel,
)
from services import env_service
from services.log_service import logger

# Anthropic Messages API 版本头，接口有变更时需要调整
ANTHROPIC_VERSION = "2023-06-01"

urls = []


async def set_urls():
    global urls
    if len(urls) > 0:
        return

    env_urls = env_service.get_chat_url()
    urls = env_urls.split(";")
    logger.info(f"anthropic urls: {urls}")


async def get_url():
    url = random.choice(urls)
    return url


async def init():
    """
    初始化函数
    """
    await set_urls()


async def get_request_url(args: BeeChatArgs):
    """
    获取请求 URL 函数
    """
    global urls
    if len(urls) == 0:
        await set_urls()

    if len(urls) == 0:
        raise ValueError("chat urls is empty")

    url = await get_url()
    return url


async def get_request_headers(token: str):
    """
    获取请求头函数

    Anthropic 使用 x-api-key 认证，而非 Authorization Bearer。
    """
    auth_key = env_service.get_auth_key() if token is None else token

    headers = {
        "Content-Type": "application/json",
        "x-api-key": f"{auth_key}",
        "anthropic-version": ANTHROPIC_VERSION,
    }
    return headers


def _split_system_and_messages(messages: list[dict]) -> tuple[str, list[dict]]:
    """把 OpenAI 的 system 消息抽出来合并为 Anthropic 的顶层 system 字段。"""
    system_parts: list[str] = []
    converted: list[dict] = []

    for message in messages:
        role = message.get("role")
        content = message.get("content")

        if role == "system":
            if isinstance(content, str):
                system_parts.append(content)
            elif isinstance(content, list):
                for part in content:
                    if part.get("type") == "text":
                        system_parts.append(part.get("text", ""))
            continue

        if role == "tool":
            # Anthropic 没有 tool 角色，工具结果要放在 user 消息的 tool_result 块里
            converted.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": message.get("tool_call_id", ""),
                    "content": content,
                }],
            })
            continue

        if role == "assistant":
            converted.append(_convert_assistant_message(message))
            continue

        converted.append({"role": "user", "content": _convert_content(content)})

    return "\n".join(system_parts), converted


def _convert_content(content):
    """把 OpenAI content（字符串或多模态列表）转换为 Anthropic content 块。"""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return content

    blocks = []
    for part in content:
        part_type = part.get("type")
        if part_type == "text":
            blocks.append({"type": "text", "text": part.get("text", "")})
        elif part_type == "image_url":
            image_url = part.get("image_url", {})
            url = image_url.get("url", "") if isinstance(image_url, dict) else image_url
            if url.startswith("data:"):
                # data:image/png;base64,xxxx
                header, data = url.split(",", 1)
                media_type = header.split(";")[0].removeprefix("data:")
                blocks.append({
                    "type": "image",
                    "source": {"type": "base64", "media_type": media_type, "data": data},
                })
            else:
                blocks.append({
                    "type": "image",
                    "source": {"type": "url", "url": url},
                })
        elif part_type in ("video_url", "input_audio", "video"):
            logger.warning(f"anthropic 不支持 {part_type} 内容块，已忽略")
        else:
            blocks.append(part)
    return blocks


def _convert_assistant_message(message: dict) -> dict:
    content = message.get("content")
    if isinstance(content, str):
        blocks = [{"type": "text", "text": content}] if content else []
    else:
        blocks = _convert_content(content)

    for tool_call in message.get("tool_calls") or []:
        function = tool_call.get("function", {})
        blocks.append({
            "type": "tool_use",
            "id": tool_call.get("id", ""),
            "name": function.get("name", ""),
            "input": _parse_json_or_empty(function.get("arguments")),
        })

    return {"role": "assistant", "content": blocks}


def _parse_json_or_empty(value):
    if not value:
        return {}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}


def _convert_tools(tools: list[dict] | None) -> list[dict] | None:
    """OpenAI tools（{"type":"function","function":{...}}）转为 Anthropic tools。"""
    if not tools:
        return None

    converted = []
    for tool in tools:
        function = tool.get("function", tool)
        converted.append({
            "name": function.get("name", ""),
            "description": function.get("description", ""),
            "input_schema": function.get("parameters", {"type": "object", "properties": {}}),
        })
    return converted


async def get_request_args(args: BeeChatArgs) -> dict:
    """OpenAI 格式参数转为 Anthropic Messages API 参数格式

    Args:
        args (BeeChatArgs): 请求参数对象

    Returns:
        dict: Anthropic Messages API 参数格式的字典对象
    """
    args_json = args.model_dump()
    system, messages = _split_system_and_messages(args_json["messages"])

    args_dict = {
        "model": args_json["model"],
        "messages": messages,
        # Anthropic 的 max_tokens 为必填，未传时给一个默认值
        "max_tokens": args_json.get("max_tokens") or 8192,
    }

    if system:
        args_dict["system"] = system
    if args_json.get("stream"):
        args_dict["stream"] = True
    if args_json.get("temperature") is not None:
        args_dict["temperature"] = args_json["temperature"]
    if args_json.get("top_p") is not None:
        args_dict["top_p"] = args_json["top_p"]
    if args_json.get("stop") is not None:
        stop = args_json["stop"]
        args_dict["stop_sequences"] = [stop] if isinstance(stop, str) else stop
    if args_json.get("tools"):
        tools = _convert_tools(args_json["tools"])
        if tools:
            args_dict["tools"] = tools

    return args_dict


def _convert_usage(usage: dict | None) -> ChatUsageModel | None:
    if not usage:
        return None

    prompt_tokens = usage.get("input_tokens", 0) or 0
    completion_tokens = usage.get("output_tokens", 0) or 0
    return ChatUsageModel(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens,
    )


def _convert_stop_reason(stop_reason: str | None) -> str | None:
    """Anthropic 停止原因转为 OpenAI 停止原因。"""
    return {
        "end_turn": "stop",
        "stop_sequence": "stop",
        "max_tokens": "length",
        "tool_use": "tool_calls",
        "refusal": "content_filter",
        "pause_turn": None,
    }.get(stop_reason)


def _extract_text(content: list[dict]) -> str:
    return "".join(
        block.get("text", "")
        for block in content
        if block.get("type") == "text"
    )


def _extract_thinking(content: list[dict]) -> str:
    return "".join(
        block.get("thinking", "")
        for block in content
        if block.get("type") == "thinking"
    )


def _extract_tool_calls(content: list[dict]) -> list[dict] | None:
    tool_calls = []
    for index, block in enumerate(content):
        if block.get("type") != "tool_use":
            continue
        tool_calls.append({
            "id": block.get("id", ""),
            "type": "function",
            "index": index,
            "function": {
                "name": block.get("name", ""),
                "arguments": json.dumps(block.get("input", {}), ensure_ascii=False),
            },
        })
    return tool_calls or None


async def get_request_result(result: dict) -> BeeChatResult:
    """获取非流式请求结果，转换为 OpenAI 格式

    Args:
        result (dict): Anthropic 返回结果

    Returns:
        BeeChatResult: 转换后的 OpenAI 格式结果对象
    """
    content = result.get("content", [])

    message = {
        "role": "assistant",
        "content": _extract_text(content),
        "reasoning_content": _extract_thinking(content) or None,
    }
    tool_calls = _extract_tool_calls(content)
    if tool_calls:
        message["tool_calls"] = tool_calls

    return BeeChatResult(
        id=result.get("id", ""),
        object="chat.completion",
        created=int(time.time()),
        model=result.get("model", ""),
        choices=[ChatChoiceModel(
            index=0,
            message=message,
            finish_reason=_convert_stop_reason(result.get("stop_reason")),
        )],
        usage=_convert_usage(result.get("usage")),
    )


async def get_request_stream_chunk_result(result: dict) -> BeeChatStreamChunkResult:
    """获取流式请求块结果，转换为 OpenAI 格式

    Anthropic 的 SSE 事件种类较多（message_start、content_block_start、
    content_block_delta、message_delta、message_stop 等），bee 的 chat 流程对
    每个事件都会调用本函数。没有文本增量的事件返回空的 delta。

    Args:
        result (dict): Anthropic 单个 SSE 事件

    Returns:
        BeeChatStreamChunkResult: 转换后的 OpenAI 格式结果对象
    """
    event_type = result.get("type")
    delta_data = {"role": None, "content": None, "reasoning_content": None}
    finish_reason = None
    usage = None

    if event_type == "content_block_start":
        block = result.get("content_block", {})
        block_type = block.get("type")
        if block_type == "text":
            delta_data["role"] = "assistant"
            delta_data["content"] = block.get("text") or None
        elif block_type == "thinking":
            delta_data["reasoning_content"] = block.get("thinking") or None
        elif block_type == "tool_use":
            delta_data["role"] = "assistant"
    elif event_type == "content_block_delta":
        delta = result.get("delta", {})
        delta_type = delta.get("type")
        if delta_type == "text_delta":
            delta_data["content"] = delta.get("text", "")
        elif delta_type == "thinking_delta":
            delta_data["reasoning_content"] = delta.get("thinking", "")
        elif delta_type == "input_json_delta":
            # 工具参数的增量片段，暂不逐片透传
            logger.debug("anthropic input_json_delta 已忽略")
    elif event_type == "message_delta":
        finish_reason = _convert_stop_reason(result.get("delta", {}).get("stop_reason"))
        usage = _convert_usage(result.get("usage"))

    return BeeChatStreamChunkResult(
        id=result.get("id", ""),
        object="chat.completion.chunk",
        created=int(time.time()),
        model=result.get("model"),
        choices=[ChatStreamChoiceModel(
            index=0,
            delta=ChatChoiceDeltaModel(**delta_data),
            finish_reason=finish_reason,
        )],
        usage=usage,
    )
