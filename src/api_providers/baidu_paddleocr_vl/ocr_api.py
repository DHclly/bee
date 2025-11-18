from api_defines.bee.models.ocr_args import OcrArgs as BeeOcrArgs
from api_defines.bee.models.ocr_result import OcrResultModel as BeeOcrResultModel
from services import env_service
from services.log_service import logger

urls=[]
url_index=0

def set_urls():
    global urls
    env_urls=env_service.get_ocr_url()
    urls=env_urls.split(";")
    logger.info(f"ocr urls: {urls}")

set_urls()

def get_url():
    global url_index
    url =urls[url_index]
    url_index=(url_index+1)%len(urls)
    return url

def get_request_url(args:BeeOcrArgs):
    global urls
    if len(urls) == 0:
        set_urls()
        
    if len(urls) == 0:
        raise ValueError("ocr urls is empty")
        
    url=get_url()
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

def get_request_args(args:BeeOcrArgs)->dict:
    """ OCR 格式参数转为当前对接平台的参数格式

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

def get_request_result(result:dict)->BeeOcrResultModel:
    """获取请求结果，转换为 OCR 格式

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
