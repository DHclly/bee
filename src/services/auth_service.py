from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services import env_service

security = HTTPBearer(auto_error=False,description="没有授权，请在右上角 Authorize 按钮传密钥")

def get_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    
    # 手动控制错误信息
    if not credentials:
        if env_service.get_api_auth() == "true":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="没有授权，请在 swagger 右上角 Authorize 按钮传密钥或者在请求头 Authorization 里面添加 Bearer 密钥",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            return None
    return credentials.credentials