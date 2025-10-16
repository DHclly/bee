from api_defines.bee.models.rerank_args import RerankArgs as BeeRerankArgs
from api_defines.bee.models.rerank_result import RerankResult as BeeRerankResult
from services import env_service


def get_request_url():
    url=env_service.get_rerank_url()
    return url

def get_request_headers(token: str):
    
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

def get_request_args(args:BeeRerankArgs)->dict:
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
    # args_dict={
    #     "model": args_json["model"],
    #     "query": args_json["query"],
    #     "documents": args_json["documents"],
    #     "top_n": args_json["top_n"],
    #     "return_documents": args_json["return_documents"]
    # }
    args_dict=args_json
    return args_dict

def get_request_result(result:dict)->BeeRerankResult:
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
    
    # result_dict = {
    #     "id": result["id"],
    #     "model": result["model"],
    #     "usage": result["usage"],
    #     "results": result["results"]
    # }
    result_dict=result
    result_obj = BeeRerankResult(**result_dict)
    return result_obj
