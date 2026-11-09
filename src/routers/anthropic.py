from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from api_defines.bee.anthropic_api import anthropic_messages
from api_defines.bee.models.anthropic_args import AnthropicArgs
from api_defines.bee.models.error_result import APIErrorResult
from services.auth_service import get_bearer_token

router = APIRouter()


@router.post(path="/v1/messages",
             tags=["Anthropic-Compatible APIs using the /v1 alias"],
             summary="Anthropic Messages 接口，兼容 Claude Messages API 格式",
             description="""兼容 Anthropic Messages API（`/v1/messages`）格式的接口，用于与 Claude 模型进行交互。

### 主要功能

- 接收 Anthropic 原生请求格式（`model`、`messages`、`max_tokens`、`system` 等）
- 支持流式响应（设置 `stream=True`）
- 流式时原样透传 Anthropic 的 SSE 事件
""",
             response_model=dict | APIErrorResult,
             responses={
                 200: {
                     "description": "成功返回 Messages 结果",
                     "content": {
                         "application/json": {
                             "example": {
                                 "id": "msg_xxx",
                                 "type": "message",
                                 "role": "assistant",
                                 "model": "claude-opus-5-5",
                                 "stop_reason": "end_turn",
                                 "content": [
                                     {"type": "text", "text": "你好，有什么可以帮你？"}
                                 ],
                                 "usage": {"input_tokens": 10, "output_tokens": 20}
                             }
                         },
                         "text/event-stream": {
                             "schema": {
                                 "type": "string",
                                 "format": "sse",
                                 "description": "SSE 流式响应，每条消息格式为 event: __\\ndata: __\\n\\n"
                             },
                             "example": """event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"你好"}}

event: message_stop
data: {"type":"message_stop"}
"""
                         }
                     }
                 }
             })
async def messages(args: AnthropicArgs, token: str = Depends(get_bearer_token)) -> dict | StreamingResponse | APIErrorResult:
    return await anthropic_messages(args, token)
