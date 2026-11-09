from pydantic import BaseModel, Field


class APIErrorResult(BaseModel):
    
    code:str = Field(
        default="000",
        description="错误码，通用错误码为，000",
        examples=["000"]
    )
    
    message: str = Field(
        "请求发生了错误",
        description="错误信息，用于描述错误的信息",
        examples=["请求发生了错误"]
    )