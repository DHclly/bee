from fastapi import APIRouter, Depends



from typing import Union

from fastapi.responses import StreamingResponse

from api_defines.bee.chat_api import chat as bee_chat
from api_defines.bee.models.chat_args import ChatArgs as BeeChatArgs
from api_defines.bee.models.chat_result import ChatResult as BeeChatResult
from api_defines.bee.models.error_result import APIErrorResult
from services.auth_service import get_bearer_token

router = APIRouter()
@router.post(path="/v1/chat/completions",
            tags=["OpenAI-Compatible APIs using the /v1 alias"],
            summary="对话补全接口，提供模型问答能力",
            description="""兼容 OpenAI API 格式的对话补全（Chat Completions）接口，用于与大语言模型进行交互。

### 主要功能

- 支持多轮对话历史（通过 `messages` 字段传递）
- 支持流式响应（设置 `stream=True`）
- 返回结构化结果，包含回复内容、token 统计、模型信息等
""",
            response_model=Union[BeeChatResult,APIErrorResult],
            responses={
                200: {
                    "description": "成功返回聊天补全结果",
                    "content": {
                        "application/json": {
                            "example": {
                                "id": "chatcmpl-WOVJFH5Rhil9xfOzqJAIC2RAqr5uNfUC",
                                "object": "chat.completion",
                                "created": 1755669269,
                                "model": "qwen2.5-7b-instruct",
                                "choices": [
                                    {
                                        "index": 0,
                                        "message": {
                                            "role": "assistant",
                                            "content": "北京、上海、广州是中国的三座超大城市，也是中国的首都北京、经济中心上海和重要的经济中心广州的简称。"
                                        },
                                        "finish_reason": "stop"
                                    }
                                ],
                                "usage": None
                            }
                        },
                        "text/event-stream": {
                            "schema": {
                                "type": "string",
                                "format": "sse",
                                "description": "SSE 流式响应，每条消息格式为 event: data: \\n\\n"
                            },
                            "example": """event: message
data: {"id":"chatcmpl-h9MoKjssEPjL4HBpdPN31ibuM83zfdXd","object":"chat.completion.chunk","created":1755739948,"model":"gguf_qwen2.5-7b","choices":[{"finish_reason":null,"index":0,"message":null,"delta":{"role":null,"content":"北","reasoning_content":null}}],"usage":null}

event: message
data: {"id":"chatcmpl-h9MoKjssEPjL4HBpdPN31ibuM83zfdXd","object":"chat.completion.chunk","created":1755739948,"model":"gguf_qwen2.5-7b","choices":[{"finish_reason":null,"index":0,"message":null,"delta":{"role":null,"content":"上","reasoning_content":null}}],"usage":null}

event: message
data: {"id":"chatcmpl-h9MoKjssEPjL4HBpdPN31ibuM83zfdXd","object":"chat.completion.chunk","created":1755739948,"model":"gguf_qwen2.5-7b","choices":[{"finish_reason":null,"index":0,"message":null,"delta":{"role":null,"content":"广","reasoning_content":null}}],"usage":null}
"""
                        }
                    }
                }
            })
async def chat(args:BeeChatArgs,token: str = Depends(get_bearer_token))->BeeChatResult | StreamingResponse | APIErrorResult:
    return await bee_chat(args,token)