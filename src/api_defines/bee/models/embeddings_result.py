from typing import Any

from pydantic import BaseModel, Field


class EmbeddingsUsageModel(BaseModel):
    """
    表示本次请求的 token 使用情况。
    """
    prompt_tokens: int | None = Field(
        0,
        description="输入文本消耗的 token 数量。",
        examples=[6]
    )
    total_tokens: int | None = Field(
        0,
        description="总共消耗的 token 数量（prompt + completion）。",
        examples=[6]
    )
    completion_tokens: int | None = Field(
        None,
        description="生成部分消耗的 token 数量。嵌入任务中通常为 0 或 null。",
        examples=[0]
    )
    prompt_tokens_details: dict[str, Any] | None = Field(
        None,
        description="提示词 token 的详细信息（如拆分、语言等），目前多数模型返回 null。",
        examples=[None]
    )


class EmbeddingsDataModel(BaseModel):
    """
    单个嵌入向量的数据项。
    """
    index: int | None = Field(
        0,
        description="对应输入文本的索引位置，用于保持顺序。",
        examples=[0]
    )
    object: str | None = Field(
        "embedding",
        description="对象类型，固定为 'embedding'。"
    )
    embedding: list[float] = Field(
        ...,
        description="生成的嵌入向量，是一个浮点数列表。",
        examples=[[-0.05364990234375, 0.005130767822265625, -0.031585693359375]]
    )


class EmbeddingsResult(BaseModel):
    """
    嵌入（Embedding）API 的标准响应模型。

    包含模型名称、生成的向量列表、唯一 ID、创建时间以及 token 使用情况。
    符合 OpenAI 兼容格式，适用于 BGE、M3 等主流嵌入模型。
    """

    id: str | None = Field(
        None,
        description="本次嵌入请求的唯一标识符，用于追踪和日志记录。",
        examples=["embd-408a45bc9703448d8926afe881821cbb"]
    )
    object: str | None = Field(
        "list",
        description="返回对象类型，固定为 'list'，表示包含多个嵌入结果。"
    )
    created: int | None = Field(
        None,
        description="时间戳（Unix 时间），表示嵌入向量生成的时间。",
        examples=[1750905855]
    )
    model: str | None = Field(
        None,
        description="实际使用的嵌入模型名称，例如 `bge-m3`。",
        examples=["bge-m3"]
    )
    data: list[EmbeddingsDataModel] = Field(
        ...,
        description="嵌入向量数据列表，每个元素对应一个输入文本。"
    )
    usage: EmbeddingsUsageModel | None = Field(
        None,
        description="本次请求的 token 使用统计信息。"
    )