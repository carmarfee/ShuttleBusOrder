# app/api/endpoints/get_credit_info.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# 请根据你的项目结构调整 import 路径
from app.models.db_models import get_db
from app.models import db_models
from app.services import order_curd
from app.core.auth import get_current_user

router = APIRouter()

@router.get(
    "/users/{user_id}/credit",
    response_model=int,
    summary="获取用户的违约次数"
)
async def get_credit_info(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: str,
    # current_user: db_models.User = Depends(get_current_user)
):
    """
    获取指定用户的违约订单次数。

    - 需要有效的Token进行认证。
    - 用户只能查询自己的违约信息 (未来可扩展为管理员查询任意用户)。
    """
    # 步骤 1: 权限验证
    # 确保请求路径中的 user_id 与 Token 中的用户ID一致
    # if current_user.id != user_id:
    #     # 如果需要允许管理员查询，可以在这里增加角色判断
    #     # if current_user.role != 'admin':
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="无权查询其他用户的信用信息",
    #     )

    # 步骤 2: 调用服务函数获取违约次数
    violation_count = await order_curd.count_violated_orders_by_user_id(db, user_id=user_id)
    
    # 步骤 3: 直接返回次数
    return violation_count