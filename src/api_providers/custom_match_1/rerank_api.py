from api_defines.bee.models.rerank_args import RerankArgs as BeeRerankArgs
from api_defines.bee.models.rerank_result import RerankResult as BeeRerankResult
from services import env_service
from services.log_service import logger
import random

urls=[]

async def set_urls():
    global urls
    if len(urls) > 0:
        return
    
    env_urls=env_service.get_rerank_url()
    urls=env_urls.split(";")
    logger.info(f"rerank urls: {urls}")

async def get_url():
    url=random.choice(urls)
    return url

async def init():
    """
    初始化函数
    """
    await set_urls()

async def get_request_url(args:BeeRerankArgs):
    """
    获取请求 URL 函数
    """
    global urls
    if len(urls) == 0:
        await set_urls()
        
    if len(urls) == 0:
        raise ValueError("rerank urls is empty")
        
    url=await get_url()
    return url

async def get_request_headers(token: str):
    """
    获取请求头函数
    """
    # 认证方式
    auth_type=env_service.get_auth_type()
    
    auth_key=None
    if token is None:
        # 认证密钥
        auth_key=env_service.get_auth_key()
    else:
        auth_key=token
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{auth_type} {auth_key}",
    }
    return headers

async def get_request_args(args:BeeRerankArgs)->dict:
    """OpenAI格式参数转为当前对接平台的参数格式

    Args:
        args (BeeRerankArgs): 请求参数对象

    Returns:
        dict: 当前对接平台的参数格式的字典对象
    """
    
    """
    openai 参数完整格式参考:
    {
        "model": "bge-reranker-v2-m3",
        "query": "苹果",
        "documents": [
            "apple",
            "苹果",
            "iPhone"
        ],
        "top_n": 10,
        "return_documents": false
    }
    """
    args_json=args.model_dump()
    # 组装为当前对接平台的参数格式
    args_dict={
        "input": {
            "query": args_json["query"],
            "documents": args_json["documents"]
        },
        "parameters": {
            "return_documents": args_json["return_documents"],
            "top_n": args_json["top_n"],
        }
    }
    return args_dict

async def get_request_result(result:dict)->BeeRerankResult:
    """获取请求结果，转换为OpenAI格式

    Args:
        result (dict): 请求参数对象

    Returns:
        BeeRerankResult: 返回的OpenAI格式的结果对象
    """
    
    """
    openai 返回结果完整格式参考:
    {
        "id": "rerank-e250b804eb174366ae77617bfeae3a65",
        "model": "jina-reranker-v2-base-multilingual",
        "usage": {
            "total_tokens": 22
        },
        "results": [
            {
            "index": 1,
            "document": {
                "text": "苹果"
            },
            "relevance_score": 0.890625
            },
            {
            "index": 2,
            "document": {
                "text": "iPhone"
            },
            "relevance_score": 0.6796875
            },
            {
            "index": 0,
            "document": {
                "text": "apple"
            },
            "relevance_score": 0.62890625
            }
        ]
    }
    """
    
    result_dict={
        "id": result["request_id"],
        "model": "bge-reranker-v2-m3",
        "usage": result["usage"],
        "results": result["output"]["results"]
    }
    result_obj = BeeRerankResult(**result_dict)
    return result_obj
