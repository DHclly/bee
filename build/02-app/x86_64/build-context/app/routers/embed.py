from fastapi import APIRouter, Depends



from typing import Union

from api_defines.bee.embeddings_api import embeddings as bee_embeddings
from api_defines.bee.models.embeddings_args import EmbeddingsArgs as BeeEmbeddingsArgs
from api_defines.bee.models.embeddings_result import (
    EmbeddingsResult as BeeEmbeddingsResult,
)
from api_defines.bee.models.error_result import APIErrorResult
from services.auth_service import get_bearer_token
router = APIRouter()

@router.post(path="/embed",
            tags=["TEI(Text Embeddings Inference) API"],
            summary="向量接口，提供生成文本嵌入向量能力",
            description="将输入的文本列表转换为对应的嵌入向量（embeddings），支持多语言和长文本。",
            response_model=Union[BeeEmbeddingsResult,APIErrorResult],
            responses={
                200: {
                    "description": "成功生成嵌入向量",
                    "content": {
                        "application/json": {
                            "example": {
                                "id": "embd-408a45bc9703448d8926afe881821cbb",
                                "object": "list",
                                "created": 1750905855,
                                "model": "bge-m3",
                                "data": [
                                    {
                                        "index": 0,
                                        "object": "embedding",
                                        "embedding": [-0.05364990234375, 0.005130767822265625, -0.031585693359375]
                                    },
                                    {
                                        "index": 1,
                                        "object": "embedding",
                                        "embedding": [-0.0276947021484375, 0.009765625, -0.037353515625]
                                    }
                                ],
                                "usage": {
                                    "prompt_tokens": 6,
                                    "total_tokens": 6,
                                    "completion_tokens": 0,
                                    "prompt_tokens_details": None
                                }
                            }
                        }
                    }
                }
            })
async def embed(args:BeeEmbeddingsArgs,token: str = Depends(get_bearer_token))->BeeEmbeddingsResult | APIErrorResult:
    return await bee_embeddings(args,token)