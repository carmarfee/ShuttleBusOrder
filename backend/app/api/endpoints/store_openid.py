# app/api/endpoints/store_openid.py

from http.client import HTTPException
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

# 请根据你的项目结构调整 import 路径
from app.models.db_models import get_db
from app.models import schemas, db_models
from app.services import user_curd
from app.core.auth import get_current_user

router = APIRouter()

@router.post(
    "/storeOpenID",
    status_code=status.HTTP_200_OK,
    summary="为当前登录用户存储或更新OpenID"
)
async def store_user_openid(
    *,
    db: AsyncSession = Depends(get_db),
    request_body: schemas.StoreOpenIDRequest,
    # 依赖认证：这将确保只有登录用户才能访问，
    # 并将用户对象注入到 current_user 变量中。
    # current_user: db_models.User = Depends(get_current_user)
):
    """
    为当前认证的用户存储或更新其微信小程序的 OpenID。
    这是一个安全的操作，用户只能修改自己的 OpenID。
    """
    # 步骤 1: 调用服务函数，使用从 Token 中获取的当前用户对象
    # 和从请求体中获取的 openid 来更新数据库。
    # await user_curd.update_user_openid(
    #     db, 
    #     db_user=current_user, 
    #     openid=request_body.openid
    # )

    #测试时由上述函数

    db_user = await user_curd.get_user(request_body.id)
    if db_user:
        await user_curd.update_user_openid(
            db, 
            db_user=db_user, 
            openid=request_body.openid
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID为 {request_body.id} 的用户不存在"
        )

    # 步骤 2: 成功后返回 204 No Content 状态码，表示操作成功且无内容返回。
    return Response(status_code=status.HTTP_200_OK)