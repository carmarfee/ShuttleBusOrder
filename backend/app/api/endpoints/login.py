# api/endpoints/login.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

# 请根据你的项目结构调整 import 路径
from app.models.db_models import get_db
from app.models import schemas
from app.services import user_curd
from app.core import security
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=schemas.LoginResponse)
async def login_for_access_token(
    *,
    db: AsyncSession = Depends(get_db),
    # 使用新的、简化的 LoginRequest 模型
    login_data: schemas.LoginRequest
):
    """
    用户登录接口 (已更新为：用户不存在则失败)。
    - **查找用户**: 根据 login_data.id 查找用户。
    - **验证失败**: 如果用户不存在，返回 404 错误。
    - **更新信息**: 如果用户存在，则用最新的信息更新他的 name 和 role。
    - **生成JWT**: 为验证通过的用户生成后端的JWT令牌。
    """
    # --- 步骤 1: 根据员工ID查找用户 ---
    user = await user_curd.get_user(db, user_id=login_data.id)
    
    # --- 步骤 2: 检查用户是否存在 ---
    if not user:
        # --- 如果用户不存在，则直接报错，不再创建用户 ---
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在，请联系管理员添加账户。",
        )
    
    # --- 步骤 3: 如果用户已存在，用最新的信息更新他 ---
    # 注意：输入中没有 phone 和 department，所以我们只更新收到的字段
    # user_update_data = schemas.UserUpdate(
    #     name=login_data.name,
    #     role=login_data.role,
    # )
    # user = await user_curd.update_user(db, db_user=user, user_in=user_update_data)

    if  login_data.password != user.password or login_data.role != user.role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户不存在，请联系管理员添加账户。:pass: {login_data.password}  | {user.password}",
        )


    # --- 步骤 4: 为验证通过的用户生成 JWT 令牌 ---
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.id, 
        expires_delta=access_token_expires
    )

    user_info = schemas.UserResponse(
        id = user.id,
        name = user.name,
        role = user.role,
        department = user.department
    )

    # --- 步骤 5: 构建并返回响应 ---
    return schemas.LoginResponse(token=access_token, userinfo=user_info)