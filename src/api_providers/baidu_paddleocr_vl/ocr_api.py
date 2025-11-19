from api_defines.bee.models.ocr_args import OcrArgs as BeeOcrArgs
from api_defines.bee.models.ocr_result import OcrResultModel as BeeOcrResultModel
from services import env_service
from services.log_service import logger
import random

urls=[]

async def set_urls():
    global urls
    if len(urls) > 0:
        return
    
    env_urls=env_service.get_ocr_url()
    urls=env_urls.split(";")
    logger.info(f"ocr urls: {urls}")

async def get_url():
    url=random.choice(urls)
    return url

async def init():
    """
    初始化函数
    """
    await set_urls()


async def get_request_url(args:BeeOcrArgs):
    """
    获取请求 URL 函数
    """
    global urls
    if len(urls) == 0:
        await set_urls()
        
    if len(urls) == 0:
        raise ValueError("ocr urls is empty")
        
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

async def get_request_args(args:BeeOcrArgs)->dict:
    """
    OCR 格式参数转为当前对接平台的参数格式函数

    Args:
        args (BeeOcrArgs): 请求参数对象

    Returns:
        dict: 当前对接平台的参数格式的字典对象
    """
    
    """
    OCR 参数完整格式参考:
    {
        "model": "deepseek-ocr",
        "file": "https://www.example.com/image.jpg",
        "text": "Free OCR."
    }
    """
    args_json=args.model_dump()
    # 组装为当前对接平台的参数格式
    args_dict={
        "stream": False,
        "temperature": 0.0,
        "model": args_json["model"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": args_json["file"]
                        }
                    },
                    {
                        "type": "text", 
                        "text": args_json["text"]
                    }
                ]
            }
        ]
    }
    
    return args_dict

async def get_request_result(result:dict)->BeeOcrResultModel:
    """
    获取当前平台请求结果，转换为 OCR 格式函数

    Args:
        result (dict): 请求参数对象

        BeeOcrResultModel: 返回的 OCR 格式的结果对象

    """
    
    """
    OCR 返回结果完整格式参考:
    {
        "text_content": "hello world",
        "json_content": {
            "text": "hello world"
        },
        "model": "deepseek-ocr",
        "cost_time": 2000
    }
    """
    result_dict = {
        "text_content": result["choices"][0]["message"]["content"],
        "json_content": {
            "text": result["choices"][0]["message"]["content"]
        },
        "model": result["model"],
        "cost_time": -1
    }
    
    result_obj = BeeOcrResultModel(**result_dict)
    return result_obj
