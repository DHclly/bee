from api_defines.bee.models.embeddings_args import EmbeddingsArgs as BeeEmbeddingsArgs
from api_defines.bee.models.embeddings_result import (
    EmbeddingsResult as BeeEmbeddingsResult,
)
from services import env_service
import os
from services.log_service import logger
import random

urls=[]

async def set_urls():
    global urls
    if len(urls) > 0:
        return
    
    env_urls=env_service.get_embeddings_url()
    urls=env_urls.split(";")
    logger.info(f"embeddings urls: {urls}")

async def get_url():
    url=random.choice(urls)
    return url

async def init():
    """
    初始化函数
    """
    await set_urls()
    
async def get_request_url(args:BeeEmbeddingsArgs):
    """
    获取请求 URL 函数
    """
    global urls
    if len(urls) == 0:
        await set_urls()
        
    if len(urls) == 0:
        raise ValueError("embeddings urls is empty")
        
    url=await get_url()
    return url

async def get_request_headers(token: str):
    
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

async def get_request_args(args:BeeEmbeddingsArgs)->dict:
    """OpenAI格式参数转为当前对接平台的参数格式

    Args:
        args (BeeEmbeddingsArgs): 请求参数对象

    Returns:
        dict: 当前对接平台的参数格式的字典对象
    """
    
    """
    openai 参数完整格式参考:
    {
        "model": "bge-m3",
        "input": [
            "apple",
            "苹果",
            "iPhone"
        ]
    }
    """
    for i in range(len(args.input)):
        input_len=len(args.input[i])
        if input_len > 4096:
            args.input[i]=args.input[i][0:4096]
            logger.warning("请求参与向量化的文本过长，文本长度{input_len}，已截断为4096字符以内")
            logger.warning(f"原始文本前100字符: {args.input[i][0:100]}")
    
    # 组装为当前对接平台的参数格式
    args_json=args.model_dump()
    # args_dict={
    #     "model": args_json["model"],
    #     "input": args_json["input"],
    # }
    args_dict=args_json
    return args_dict

async def get_request_result(result:dict)->BeeEmbeddingsResult:
    """获取请求结果，转换为OpenAI格式

    Args:
        result (dict): 请求参数对象

    Returns:
        BeeEmbeddingsResult: 返回的OpenAI格式的结果对象
    """
    
    """
    openai 返回结果完整格式参考:
    {
        "id": "embd-408a45bc9703448d8926afe881821cbb",
        "object": "list",
        "created": 1750905855,
        "model": "bge-m3",
        "data": [
            {
                "index": 0,
                "object": "embedding",
                "embedding": [-0.05364990234375, 0.005130767822265625, -0.031585693359375]
            },
            {
                "index": 1,
                "object": "embedding",
                "embedding": [-0.0276947021484375, 0.009765625, -0.037353515625]
            }
        ],
        "usage": {
            "prompt_tokens": 6,
            "total_tokens": 6,
            "completion_tokens": 0,
            "prompt_tokens_details": None
        }
    }
    """
    
    # result_dict = {
    #     "id": result["id"],
    #     "object": result["object"],
    #     "created": result["created"],
    #     "model": result["model"],
    #     "usage": result["usage"],
    #     "data": result["data"]
    # }
    result_dict=result
    result_obj = BeeEmbeddingsResult(**result_dict)
    return result_obj
