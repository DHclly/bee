import os


def get_auth_type():
    return os.getenv('bee_auth_type', 'Bearer')

def get_auth_key():
    return os.getenv('bee_auth_key', 'sk_123')

def get_embeddings_url():
    # 支持英文的分号;分隔
    return os.getenv('bee_embeddings_url', 'http://localhost/v1/embeddings')

def get_rerank_url():
    # 支持英文的分号;分隔
    return os.getenv('bee_rerank_url', 'http://localhost/v1/rerank')

def get_chat_url():
    # 支持英文的分号;分隔
    return os.getenv('bee_chat_url', 'http://localhost/v1/chat/completions')

def get_ocr_url():
    # 支持英文的分号;分隔
    return os.getenv('bee_ocr_url', 'http://localhost/v1/chat/completions')

def get_asr_url():
    # 支持英文的分号;分隔
    return os.getenv('bee_asr_url', 'http://localhost/v1/chat/completions')

def get_tts_url():
    # 支持英文的分号;分隔
    return os.getenv('bee_tts_url', 'http://localhost/v1/chat/completions')

def get_provider_type():
    return os.getenv('bee_provider_type', 'gpustack')

def get_show_swagger():
    return os.getenv('bee_show_swagger', 'true')

def get_show_redoc():
    return os.getenv('bee_show_redoc', 'true')

def get_log_level():
    return os.getenv('bee_log_level', 'info')

def get_bee_workers():
    return os.getenv('bee_workers', '1')

def get_env(env_name):
    return os.getenv(env_name, '')