from api_defines.bee.models.chat_args import ChatArgs as BeeChatArgs
from api_defines.bee.models.chat_result import ChatResult as BeeChatResult
from api_defines.bee.models.chat_result import (
    ChatStreamChunkResult as BeeChatStreamChunkResult,
)
from services import env_service


def get_request_url():
    url=env_service.get_chat_url()
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

def get_request_args(args:BeeChatArgs)->dict:
    """OpenAI格式参数转为当前对接平台的参数格式

    Args:
        args (BeeChatArgs): 请求参数对象

    Returns:
        dict: 当前对接平台的参数格式的字典对象
    """
    
    """
    openai 参数完整格式参考:
    {
        "stream": true,
        "temperature": 1,
        "top_p": 1,
        "max_tokens": 16384,
        "model": "qwen2.5-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "你是一位超级厉害的导游，精通中国各个城市信息"
            },
            {
                "role": "user",
                "content": "北上广是哪里"
            }
        ]
    }
    """
    # 组装为当前对接平台的参数格式
    args_json=args.model_dump()
    # args_dict={
    #     "model": args_json["model"],
    #     "messages":args_json["messages"],
    #     "stream": args_json["stream"],
    #     "stream_options": args_json["stream_options"],
    #     "temperature": args_json["temperature"],
    #     "top_p": args_json["top_p"],
    #     "max_tokens": args_json["max_tokens"],
    #     "presence_penalty": args_json["presence_penalty"],
    #     "frequency_penalty": args_json["frequency_penalty"],
    #     "stop": args_json["stop"],
    #     "seed": args_json["seed"]
    # }
    args_dict=args_json
    return args_dict

def get_request_result(result:dict)->BeeChatResult:
    """获取非流式请求结果，转换为OpenAI格式

    Args:
        result (dict): 请求参数对象

    Returns:
        BeeChatResult: 返回的OpenAI格式的结果对象
    """
    
    """
    openai 返回结果完整格式参考:
    {
        "id": "chatcmpl-WOVJFH5Rhil9xfOzqJAIC2RAqr5uNfUC",
        "object": "chat.completion",
        "created": 1755669269,
        "model": "qwen2.5-7b-instruct",
        "choices": [
            {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "北京、上海、广州是中国的三座超大城市，也是中国的首都北京、经济中心上海和重要的经济中心广州的简称。"
            },
            "finish_reason": "stop"
            }
        ]
    }
    """
    # result_dict = {
    #     "id": result["id"],
    #     "object": result["object"],
    #     "created": result["created"],
    #     "model": result["model"],
    #     "usage": result["usage"],
    #     "choices": result["choices"]
    # }
    result_dict=result
    result_obj = BeeChatResult(**result_dict)
    return result_obj

def get_request_stream_chunk_result(result:dict)->BeeChatStreamChunkResult:
    """获取流式请求块结果，转换为OpenAI格式

    Args:
        result (dict): 请求参数对象

    Returns:
        BeeChatStreamChunkResult: 返回的OpenAI格式的结果对象
    """
    
    """
    openai 返回结果完整格式参考:
    {
        "id": "chatcmpl-SBT7AeDAoKp19yu0WggtDDbJN5HOJ2Ny",
        "object": "chat.completion.chunk",
        "created": 1755739080,
        "model": "gguf_qwen2.5-7b",
        "choices": [
            {
                "finish_reason": null,
                "index": 0,
                "message": null,
                "delta": {
                    "role": null,
                    "content": "北",
                    "reasoning_content": null
                }
            }
        ],
        "usage": null
    }
    {
        "id": "chatcmpl-SBT7AeDAoKp19yu0WggtDDbJN5HOJ2Ny",
        "object": "chat.completion.chunk",
        "created": 1755739080,
        "model": "gguf_qwen2.5-7b",
        "choices": [
            {
                "finish_reason": null,
                "index": 0,
                "message": null,
                "delta": {
                    "role": null,
                    "content": "上",
                    "reasoning_content": null
                }
            }
        ],
        "usage": null
    }
    """
    # result_dict = {
    #     "id": result["id"],
    #     "object": result["object"],
    #     "created": result["created"],
    #     "model": result["model"],
    #     "usage": result["usage"],
    #     "choices": result["choices"]
    # }
    result_dict=result
    result_obj = BeeChatStreamChunkResult(**result_dict)
    return result_obj