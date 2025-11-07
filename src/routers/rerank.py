from fastapi import APIRouter, Depends

from api_defines.bee.models.error_result import APIErrorResult
from api_defines.bee.models.rerank_args import RerankArgs as BeeRerankArgs
from api_defines.bee.models.rerank_result import RerankResult as BeeRerankResult
from api_defines.bee.rerank_api import rerank as bee_rerank
from services.auth_service import get_bearer_token
from typing import Dict, Any, Union

router = APIRouter()

summary="重排接口，提供文本相关性重排序能力"
description=(
        "对给定查询（query）与一组候选文档（documents）进行语义相关性重排序。"
        "适用于检索增强生成（RAG）、搜索结果排序等场景"
        "返回结果按相关性得分降序排列，并包含原始索引以便映射。"
    )
response_model:Any=BeeRerankResult|APIErrorResult
responses:Dict[Union[int, str], Dict[str, Any]]={
    200: {
        "description": "成功完成重排序，返回按相关性得分排序的结果列表",
        "content": {
            "application/json": {
                "example": {
                    "id": "rerank-e9ecfce472394c5b859086365d6b63b9",
                    "model": "bge-reranker-v2-m3",
                    "usage": {
                        "total_tokens": 13
                    },
                    "results": [
                        {
                            "index": 0,
                            "document": {
                                "text": "苹果"
                            },
                            "relevance_score": 0.9083984375
                        },
                        {
                            "index": 1,
                            "document": {
                                "text": "apple"
                            },
                            "relevance_score": 0.5141143798828125
                        },
                        {
                            "index": 2,
                            "document": {
                                "text": "iPhone"
                            },
                            "relevance_score": 0.3141143
                        }
                    ]
                }
            }
        }
    }
}

@router.post(
    path="/v1/rerank",
    tags=["OpenAI-Compatible APIs using the /v1 alias"],
    summary=summary,
    description=description,
    response_model=response_model,
    responses=responses
)
@router.post(
    path="/rerank",
    tags=["Rerank API"],
    summary=summary,
    description=description,
    response_model=response_model,
    responses=responses
)
async def rerank(args: BeeRerankArgs,token: str = Depends(get_bearer_token))->BeeRerankResult | APIErrorResult:
    return await bee_rerank(args,token)