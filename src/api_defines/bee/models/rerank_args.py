
from pydantic import BaseModel, Field, field_validator


class RerankArgs(BaseModel):
    """
    请求参数模型：用于文本重排序（Rerank）API。

    该模型定义了调用重排序模型所需的基本参数，包括模型名称、查询文本、候选文档列表以及返回的最优结果数量。
    """

    model: str = Field(
        ...,
        description="要使用的重排序模型名称，例如 `bge-reranker-v2-m3`",
        examples=["bge-reranker-v2-m3"]
    )
    query: str = Field(
        ...,
        description="查询文本，用于与文档进行相关性排序。",
        min_length=1,
        examples=["苹果"]
    )
    documents: list[str] = Field(
        ...,
        description="候选文档列表，将根据与 query 的相关性进行重排序。不能为空。",
        min_length=1,
        examples=[["apple", "苹果","iPhone"]]
    )
    top_n: int | None = Field(
        default=None,
        description=(
            "排序返回的top文档数量，未指定时默认返回全部候选文档，"
            "如果指定的top_n值大于输入的候选document数量，返回全部候选文档"
        ),
        ge=1,
        examples=[10]
    )
    
    return_documents:bool | None=Field(
        default=False,
        description="返回的排序结果列表中是否返回每一条document原文，默认值 False",
        examples=[False]
    )

    @field_validator("documents")
    @classmethod
    def documents_must_not_be_empty(cls, value: list[str]) -> list[str]:
        """
        验证 documents 列表不能为空。

        Args:
            value (List[str]): 输入的文档列表。

        Returns:
            List[str]: 验证通过的列表。

        Raises:
            ValueError: 如果列表为空，抛出此异常。
        """
        if not value:
            raise ValueError("documents cannot be empty")
        return value

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, value: str) -> str:
        """
        验证 query 字符串不能为空。

        Args:
            value (str): 查询文本。

        Returns:
            str: 验证通过的查询文本。

        Raises:
            ValueError: 如果字符串为空或仅空白字符，抛出此异常。
        """
        if not value.strip():
            raise ValueError("query cannot be empty or whitespace")
        return value