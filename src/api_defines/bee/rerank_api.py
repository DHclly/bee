
from services.http_service import http_clients
from services.log_service import logger
from services.module_load_service import load_rerank_api

from .models.error_result import APIErrorResult
from .models.rerank_args import RerankArgs as BeeRerankArgs
from .models.rerank_result import RerankResult as BeeRerankResult
import asyncio

rerank_api=None
rerank_api_initialized = False
rerank_api_lock = asyncio.Lock()

async def rerank(args:BeeRerankArgs,token: str)->BeeRerankResult | APIErrorResult:
    response=None
    global rerank_api, rerank_api_initialized
    try:
        if not rerank_api_initialized:
            async with rerank_api_lock:
                if not rerank_api_initialized:
                    rerank_api = load_rerank_api()
                    await rerank_api.init() # type: ignore
                    rerank_api_initialized=True
                    
        request_url= await rerank_api.get_request_url(args) # type: ignore
        request_headers = await rerank_api.get_request_headers(token) # type: ignore
        request_args = await rerank_api.get_request_args(pre_process_args(args)) # type: ignore
        
        logger.info(f"发起重排请求,地址:{request_url}\n")
        logger.debug(f"请求头参数：{request_headers}\n")
        logger.debug(f"原始请求参数：{args.model_dump_json()}\n")
        logger.debug(f"修改后请求参数：{request_args}\n")
        
        client=http_clients.rerank_client
        response = await client.post(url=request_url,headers=request_headers,json=request_args)
        response.raise_for_status()
        result_data = response.json()
        logger.debug(f"原始返回参数：{result_data}\n")
        result = await rerank_api.get_request_result(result_data) # type: ignore
        logger.debug(f"修改后返回参数：{result.model_dump_json()}\n")
        logger.info("重排请求成功")
        return result
    except Exception as e:
        response_text=""
        if response:
            response_text=",响应信息："+response.text
        error_text=f"重排请求发生错误，异常类型：{str(type(e))},异常信息：{e} {response_text}"
        logger.error(error_text)
        return APIErrorResult(message=error_text)


def pre_process_args(args:BeeRerankArgs)->BeeRerankArgs:
    doc_len=len(args.documents)
    top_n=args.top_n
    if top_n is None:
        return args
    
    if top_n>=doc_len or top_n<=0:
        args.top_n=doc_len
    
    return args