
from pydantic import BaseModel, Field, field_validator

class UploadResult(BaseModel):
    """
    上传完成的结果
    """

    success: bool = Field(
        False,
        description="是否上传成功",
        examples=["False"]
    )
    
    file_id: str = Field(
        "",
        description="上传成功后的文件名称",
        examples=[["60e0a011492044d991236c6f6a9a5dd7"]]
    )
    
    message: str = Field(
        "",
        description="上传失败的原因",
        examples=["文件类型不支持"] 
    )
    
class DeleteResult(BaseModel):
    """
    删除完成的结果
    """

    success: bool = Field(
        False,
        description="是否删除成功",
        examples=["False"]
    )
    
    message: str = Field(
        "",
        description="删除失败的原因",
        examples=["文件不存在"] 
    )