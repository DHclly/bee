from api_defines.bee.models.embeddings_args import EmbeddingsArgs as BeeEmbeddingsArgs
from api_defines.bee.models.embeddings_result import (
    EmbeddingsResult as BeeEmbeddingsResult,
)
from services import env_service, time_service, uuid_service


async def get_request_url(args:BeeEmbeddingsArgs):
    url=env_service.get_embeddings_url()
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
    # 组装为当前对接平台的参数格式
    args_json=args.model_dump()
    args_dict={
        "model": args_json["model"],
        "inputs": args_json["input"],
    }
    
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
    
    result_dict = {
        "id": f"embed-{uuid_service.get_uuid()}",
        "object": "list",
        "created": time_service.get_current_timestamp_int(),
        "model": "embed",
        "usage": None,
        "data": [{
                "index": index,
                "object": "embedding",
                "embedding": embedding
            } for index,embedding in enumerate(result)]
    }
    
    result_obj = BeeEmbeddingsResult(**result_dict)
    return result_obj
