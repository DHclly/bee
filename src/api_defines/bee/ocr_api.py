from services.http_service import http_clients
from services.log_service import logger
from services.module_load_service import load_ocr_api
from api_defines.bee.models.ocr_args import OcrArgs as BeeOcrArgs
from api_defines.bee.models.ocr_result import OcrResultModel as BeeOcrResultModel
from .models.error_result import APIErrorResult

ocr_api=None

async def ocr(args:BeeOcrArgs,token: str)->BeeOcrResultModel|APIErrorResult:
    
    response=None
    try:
        global ocr_api
        if ocr_api is None:
            ocr_api=load_ocr_api()
        
        request_url=ocr_api.get_request_url(args)
        request_headers = ocr_api.get_request_headers(token)
        request_args = ocr_api.get_request_args(pre_process_args(args))
        
        logger.info(f"发起文字识别请求,地址:{request_url}\n")
        logger.debug(f"请求头参数：{request_headers}\n")
        logger.debug(f"原始请求参数：{args.model_dump_json()}\n")
        logger.debug(f"修改后请求参数：{request_args}\n")
        
        client=http_clients.chat_client
        response = await client.post(url=request_url,headers=request_headers,json=request_args)
        response.raise_for_status()
        result_data = response.json()
        logger.debug(f"原始返回参数：{result_data}\n")
        result = ocr_api.get_request_result(result_data)
        logger.debug(f"修改后返回参数：{result.model_dump_json()}\n")
        logger.info("文字识别请求成功")
        return result
    except Exception as e:
        response_text=""
        if response:
            response_text=",响应信息："+response.text
        error_text=f"文字识别请求发生错误，异常类型：{str(type(e))},异常信息：{e} {response_text}"
        logger.error(error_text)
        return APIErrorResult(message=error_text)
    
def pre_process_args(args:BeeOcrArgs)->BeeOcrArgs:
    return args