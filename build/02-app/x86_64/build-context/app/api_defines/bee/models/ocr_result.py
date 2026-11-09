
from pydantic import BaseModel, Field


class OcrResultModel(BaseModel):
    """
    表示 OCR 识别结果。
    """
    text_content: str = Field(
        ...,
        description="OCR识别出的文本内容。",
        examples=["hello world"]
    )
    
    json_content: dict|None = Field(
        None,
        description="OCR识别出的文本内容的json格式数据。",
        examples=[{"text": "hello world"}]
    )
    
    model: str|None = Field(
        None,
        description="使用的 OCR 模型名称，例如 `deepseek-ocr`、`paddleocr`、`paddleocr-vl`",
        examples=["deepseek-ocr"]
    )