
from pydantic import BaseModel, Field, field_validator


class EmbeddingsArgs(BaseModel):
    """
    请求参数模型：用于文本嵌入（Embedding）API。

    该模型定义了调用嵌入模型所需的基本参数，包括模型名称和待处理的文本列表。
    """

    model: str = Field(
        ...,
        description="要使用的嵌入模型名称，例如 `bge-m3`",
        examples=["bge-m3"]
    )
    input: list[str] = Field(
        ...,
        description="生成嵌入向量的字符串列表。不能为空。",
        min_length=1,  # 配合 validator 双重保障
        examples=[["apple", "苹果","iPhone"]]
    )

    @field_validator("input")
    @classmethod
    def input_must_not_be_empty(cls, value):
        """
        验证 input 列表不能为空。

        Args:
            value (List[str]): 输入的文本列表。

        Returns:
            List[str]: 验证通过的列表。

        Raises:
            ValueError: 如果列表为空，抛出此异常。
        """
        if not value:  # 检查是否为空列表 []
            raise ValueError("input cannot be empty")
        return value