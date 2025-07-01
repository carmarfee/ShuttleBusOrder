# app/core/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from pydantic import ValidationError

# 导入你的项目模块
from app.core.config import settings
from app.models.db_models import get_db
from app.models import schemas, db_models
from app.services import user_curd

# 1. 创建 OAuth2PasswordBearer 实例
#    tokenUrl 指向你获取 token 的登录接口路径。
#    这主要用于 OpenAPI (Swagger UI) 文档，让它知道去哪里获取令牌。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> db_models.User:
    """
    一个依赖项，用于：
    1. 从请求头中提取 JWT。
    2. 解码并验证 JWT。
    3. 从数据库中获取用户。
    4. 返回用户对象。
    如果任何步骤失败，都会抛出 HTTP 401 错误。
    """
    # 定义一个标准的认证失败异常
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 2. 解码 JWT
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # 3. 从 payload 中获取用户ID (我们在创建 token 时用 'sub' 字段存储了它)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        # 如果 token 过期或无效，jose 库会抛出 JWTError
        raise credentials_exception

    # 4. 从数据库中获取用户
    user = await user_curd.get_user(db, user_id=user_id)
    if user is None:
        # 如果 token 中的用户ID在数据库中找不到
        raise credentials_exception
        
    # 5. 返回数据库中的用户模型对象
    return user

def get_current_admin_user(
    current_user: db_models.User = Depends(get_current_user)
) -> db_models.User:
    """
    一个依赖项，用于验证当前用户是否为管理员。
    如果不是管理员，则抛出 HTTP 403 错误。
    """
    # 假设管理员的角色名称是 'admin'
    # 你可以根据需要在 config.py 中将其定义为配置项
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="操作未授权：需要管理员权限"
        )
    return current_user