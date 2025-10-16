
from services.http_service import http_clients
from services.log_service import logger
from services.module_load_service import load_embeddings_api

from .models.embeddings_args import EmbeddingsArgs as BeeEmbeddingsArgs
from .models.embeddings_result import EmbeddingsResult as BeeEmbeddingsResult
from .models.error_result import APIErrorResult

embeddings_api=load_embeddings_api()

async def embeddings(args:BeeEmbeddingsArgs,token: str)->BeeEmbeddingsResult | APIErrorResult:
    response=None
    try:
        request_url=embeddings_api.get_request_url()
        request_headers = embeddings_api.get_request_headers(token)
        request_args = embeddings_api.get_request_args(pre_process_args(args))
        
        logger.info(f"发起文本嵌入请求,地址:{request_url}\n")
        logger.debug(f"请求头参数：{request_headers}\n")
        logger.debug(f"原始请求参数：{args.model_dump_json()}\n")
        logger.debug(f"修改后请求参数：{request_args}\n")
        
        client=http_clients.embeddings_client
        response = await client.post(url=request_url,headers=request_headers,json=request_args)
        response.raise_for_status()
        result_data = response.json()
        logger.debug(f"原始返回参数：{result_data}\n")
        result = embeddings_api.get_request_result(result_data)
        logger.debug(f"修改后返回参数：{result.model_dump_json()}\n")
        logger.info("文本嵌入请求成功")
        return result
    except Exception as e:
        response_text=""
        if response:
            response_text=",响应信息："+response.text
        error_text=f"文本嵌入请求发生错误，异常类型：{str(type(e))},异常信息：{e} {response_text}"
        logger.error(error_text)
        return APIErrorResult(message=error_text)


def pre_process_args(args:BeeEmbeddingsArgs)->BeeEmbeddingsArgs:
    return args