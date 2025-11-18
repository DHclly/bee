
from pydantic import BaseModel, Field, field_validator


class OcrArgs(BaseModel):
    """
    请求参数模型：用于文字识别（OCR）API。

    该模型定义了调用 OCR 模型所需的基本参数。
    """

    model: str = Field(
        ...,
        description="要使用的 OCR 模型名称，例如 `deepseek-ocr`、`paddleocr`、`paddleocr-vl`",
        examples=["deepseek-ocr"]
    )
    
    file: str = Field(
        ...,
        description="要进行OCR的文件路径，支持 base64 编码的图片字符串或图片URL",
        examples=["https://www.example.com/image.jpg"]
    )
    
    text: str = Field(
        "Free OCR.",
        description="要使用模型的提示词，例如 deepseek-ocr 模型的提示词 `Free OCR.`",
        examples=["Free OCR."]
    )