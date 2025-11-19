from fastapi import APIRouter, File, Form, UploadFile,Query,Path as FastAPIPath
from fastapi.responses import Response
from typing import Union,Annotated
from pathlib import Path
from urllib.parse import quote
import mimetypes
from api_defines.bee.file_storage_api import upload as bee_upload,delete as bee_delete,download as bee_download
from api_defines.bee.models.file_storage_result import UploadResult as BeeUploadResult,DeleteResult as BeeDeleteResult
from api_defines.bee.models.error_result import APIErrorResult
from services import uuid_service

router = APIRouter()

@router.post(path="/file/upload",
            tags=["File Storage API"],
            summary="上传文件",
            description="上传一个文件，并返回文件 ID",
            response_model=BeeUploadResult,
            responses={
                200: {
                    "description": "上传成功",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "file_id": "1ca5b88aed304133bc4e682976970347",
                                "message": "上传成功"
                            }
                        }
                    }
                }
            })
async def upload(upload_file: UploadFile = File(...))->BeeUploadResult:
    try:
        suffix=""
        if upload_file.filename is not None:
            suffix=Path(upload_file.filename).suffix
        file_id=uuid_service.get_uuid()
        file_name=f"{file_id}{suffix}"
        file_content:bytes=await upload_file.read()
        await bee_upload(file_id,file_name,file_content)
        return BeeUploadResult(success=True,file_id=file_id,message="上传成功")
    except Exception as e:
        return BeeUploadResult(success=False,file_id="error",message="上传失败:"+str(e))

@router.delete(path="/file/delete/{file_id}",
            tags=["File Storage API"],
            summary="删除文件",
            description="根据文件ID删除已上传的文件",
            response_model=Union[BeeDeleteResult],
            responses={
                200: {
                    "description": "删除成功",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "message": "删除成功"
                            }
                        }
                    }
                }
            })
async def delete(file_id:str = FastAPIPath(..., description="文件的唯一标识符", min_length=1))->BeeDeleteResult:
    try:
        await bee_delete(file_id)
        return BeeDeleteResult(success=True,message="删除成功")
    except Exception as e:
        return BeeDeleteResult(success=False,message="删除失败:"+str(e))

@router.get(path="/file/download/{file_id}",
            tags=["File Storage API"],
            summary="获取文件下载地址",
            description="根据文件ID获取文件的下载URL"
            )
async def download(file_id:str = FastAPIPath(..., description="文件的唯一标识符", min_length=1),
                   force_download: bool = Query(True, description="是否强制浏览器下载（而非预览）")
                   )-> Response:
    
    file_name,file_content= await bee_download(file_id)
    
    if file_name=="not_found":
        return Response(
            content=file_content,
            media_type="plain/text"
        )
    
    mime_type, _ = mimetypes.guess_type(file_name)
    mime_type = mime_type or "application/octet-stream"
    content_disposition=None
    
    # UTF-8 编码的文件名
    encodeFileName = quote(file_name, safe='')
    if force_download:
        mime_type = "application/octet-stream"
        content_disposition = f'attachment;filename={encodeFileName};filename*=utf-8\'\'{encodeFileName};"'
        
    return Response(
            content=file_content,
            media_type=mime_type ,
            headers={"Content-Disposition": content_disposition} if content_disposition else {}
        )