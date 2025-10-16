import importlib
from types import ModuleType

from services import env_service
from services.log_service import logger


def load_api_provider_api(provider_name: str,method_name:str) -> ModuleType:
    """
    动态加载 api_providers 下指定 provider_name 的 method_name 函数
    """
    module_path = f"api_providers.{provider_name}"
    logger.info(f"加载服务 {provider_name} 的模块 {method_name}")
    try:
        # 动态导入模块
        module = importlib.import_module(module_path)
        # 获取 rerank_api 函数
        rerank_api = getattr(module,method_name, None)
        
        if rerank_api is None:
            raise AttributeError(f"模块 {module_path} 中没有 '{method_name}' 函数")
        
        return rerank_api
    
    except ImportError as e:
        raise ImportError(f"无法导入模块 {module_path}: {e}")
    
    except Exception as e:
        raise RuntimeError(f"加载 {provider_name} 的 {method_name} 失败: {e}")
    
def load_rerank_api() -> ModuleType:
    provider_name=env_service.get_provider_type()
    return load_api_provider_api(provider_name,"rerank_api")
    
def load_embeddings_api() -> ModuleType:
    provider_name=env_service.get_provider_type()
    return load_api_provider_api(provider_name,"embeddings_api")
    
def load_chat_api() -> ModuleType:
    provider_name=env_service.get_provider_type()
    return load_api_provider_api(provider_name,"chat_api")