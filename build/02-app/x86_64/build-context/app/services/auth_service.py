from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(auto_error=False,description="模型 API 密钥,如：sk-xxxxxx")

def get_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security))->str:
    # 没有秘钥就返回默认值
    if not credentials:
        return "sk-default"
    return credentials.credentials