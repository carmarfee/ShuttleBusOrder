# /backend/app/utils/security.py

# --- 1. 修正这里的 import 语句 ---
from datetime import datetime,timedelta,timezone
from jose import jwt
from typing import Any
from passlib.context import CryptContext
from app.core.config import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """
    为指定的主题（subject）创建一个新的JWT访问令牌。
    """
    if expires_delta:
        # 如果提供了过期时间增量，则使用它
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 否则，使用配置文件中的默认过期时间
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY, # 确保你的配置中是 JWT_SECRET_KEY
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

# 如果你还需要一个函数来解码令牌，可以像下面这样添加
def verify_access_token(token: str):
    # ... 在这里实现解码和验证逻辑 ...
    pass

def get_password_hash(password: str) -> str:
    """
    为明文密码生成哈希值。
    """
    return pwd_context.hash(password)