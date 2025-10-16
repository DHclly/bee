import os


def get_auth_type():
    return os.getenv('bee_auth_type', 'Bearer')

def get_auth_key():
    return os.getenv('bee_auth_key', 'sk_123')

def get_embeddings_url():
    return os.getenv('bee_embeddings_url', 'http://localhost')

def get_rerank_url():
    return os.getenv('bee_rerank_url', 'http://localhost')

def get_chat_url():
    return os.getenv('bee_chat_url', 'http://localhost')

def get_provider_type():
    return os.getenv('bee_provider_type', 'default')

def get_show_swagger():
    return os.getenv('bee_show_swagger', 'true')

def get_show_redoc():
    return os.getenv('bee_show_redoc', 'true')

def get_api_auth():
    return os.getenv('bee_api_auth', 'true')

def get_log_level():
    return os.getenv('bee_log_level', 'info')