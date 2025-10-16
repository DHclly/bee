
from pydantic import BaseModel, Field


class RerankDocumentModel(BaseModel):
    """
    表示一个被重排序的文档对象。
    """
    text: str = Field(
        ...,
        description="文档的原始文本内容。",
        examples=["apple"]
    )


class RerankResultModel(BaseModel):
    """
    表示重排序结果中的单个条目。
    """
    index: int | None = Field(
        0,
        description="该文档在原始输入 documents 列表中的索引位置。",
        ge=0,
        examples=[0]
    )
    document: RerankDocumentModel | None = Field(
        None,
        description="对应的文档内容。"
    )
    relevance_score: float = Field(
        0.0,
        description="文档与查询 query 的相关性得分，值越高表示越相关。",
        ge=0.0,
        examples=[0.1083984375]
    )


class RerankUsageModel(BaseModel):
    """
    表示本次请求的资源使用情况。
    """
    total_tokens: int | None = Field(
        0,
        description="本次请求总共消耗的 token 数量。",
        ge=0,
        examples=[13]
    )


class RerankResult(BaseModel):
    """
    重排序（Rerank）API 的响应结果模型。

    该模型封装了重排序的完整返回数据，包括唯一 ID、使用情况、模型名称和排序后的结果列表。
    """

    id: str | None = Field(
        None,
        description="本次重排序请求的唯一标识符。",
        examples=["rerank-e9ecfce472394c5b859086365d6b63b9"]
    )
    model: str | None = Field(
        None,
        description="用于重排序的模型名称。",
        examples=["bge-reranker-v2-m3"]
    )
    usage: RerankUsageModel | None = Field(
        None,
        description="本次请求的资源使用统计。"
    )
    results: list[RerankResultModel] = Field(
        ...,
        description="按相关性得分降序排列的结果列表，包含原始索引、文档内容和得分。",
        min_length=1
    )