from fastapi import APIRouter, Depends



from typing import Union

from fastapi.responses import StreamingResponse

from api_defines.bee.ocr_api import ocr as bee_ocr
from api_defines.bee.models.ocr_args import OcrArgs as BeeOcrArgs
from api_defines.bee.models.ocr_result import OcrResultModel as BeeOcrResultModel
from api_defines.bee.models.error_result import APIErrorResult
from services.auth_service import get_bearer_token

router = APIRouter()
@router.post(path="/ocr",
            tags=["OCR(Optical Character Recognition) API"],
            summary="光学字符识别接口，提供图片文字识别能力",
            description="""
            
""",
            response_model=Union[BeeOcrResultModel,APIErrorResult],
            responses={
                200: {
                    "description": "成功返回文字识别结果",
                    "content": {
                        "application/json": {
                            "example": {
                                "text_content": "hello world",
                                "json_content":{"text": "hello world"},
                                "model": "deepseek-ocr",
                                "cost_time":2000
                            }
                        }
                    }
                }
            })
async def ocr(args:BeeOcrArgs,token: str = Depends(get_bearer_token))->BeeOcrResultModel|APIErrorResult:
    return await bee_ocr(args,token)