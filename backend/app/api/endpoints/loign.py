# api/v1/endpoints/login.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database.session import get_db
from app.models import schemas
from app.services import crud_user
from app.utils import security
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    *,
    db: Session = Depends(get_db),
    login_data: schemas.LoginRequest
):
    """
    用户登录接口，处理企业认证信息并返回JWT令牌。

    - **验证企业令牌**: (当前为模拟) 验证 `login_data.token` 的有效性。
    - **获取 OpenID**: (当前为模拟) 使用 `login_data.code` 向微信服务器换取 `openid`。
    - **查找或创建用户**: 根据员工ID查找用户，如果不存在则创建新用户。
    - **绑定 OpenID**: 如果用户已存在但未绑定微信，则进行绑定。
    - **生成并返回JWT**: 为该用户生成一个后端专用的JWT令牌。
    """
    # --- 步骤 1: (模拟) 验证企业令牌的有效性 ---
    # 在真实场景中，你需要调用企业认证系统的接口来验证这个token
    # 这里我们假设它总是有效的
    if not login_data.token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="企业认证令牌无效",
        )

    # --- 步骤 2: (模拟) 使用 code 换取 openid ---
    # 在真实场景中，你需要使用 httpx 或 requests 库向微信API发送请求
    # url = f"https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={login_data.code}&grant_type=authorization_code"
    # 这里我们模拟一个 openid
    mock_openid = f"mock_openid_for_{login_data.userinfo.id}"
    
    # --- 步骤 3: 根据员工ID查找用户 ---
    user = crud_user.get_user_by_employee_id(db, employee_id=login_data.userinfo.id)
    
    if user:
        # 如果用户存在，检查是否已绑定 openid
        if not user.openid:
            # 如果未绑定，则更新 openid
            crud_user.update_user_openid(db, db_user=user, openid=mock_openid)
    else:
        # 如果用户不存在，则创建新用户
        user = crud_user.create_user(db=db, openid=mock_openid, user_info=login_data.userinfo)

    # --- 步骤 4: 生成 JWT 令牌 ---
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.employee_id, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
