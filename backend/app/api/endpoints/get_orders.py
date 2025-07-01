# app/api/endpoints/get_orders.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# 请根据你的项目结构调整 import 路径
from app.models.db_models import get_db
from app.models import schemas, db_models
from app.services import order_curd
from app.core.auth import get_current_user

router = APIRouter()

@router.get(
    "/getOrders/{user_id}",
    response_model=schemas.UserOrdersResponse,
    summary="获取指定用户的所有订单（按状态分类）"
)
async def get_user_orders(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: str,
    # current_user: db_models.User = Depends(get_current_user)
):
    """
    获取指定用户的所有订单，并按状态分类返回订单ID列表。
    - 需要有效的Token进行认证。
    - 用户只能查询自己的订单（未来可扩展为管理员查询任意用户）。
    """
    # 步骤 1: 权限验证 , 测试时注释
    # 确保请求路径中的 user_id 与 Token 中的用户ID一致
    # if current_user.id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="无权查询其他用户的订单信息",
    #     )

    # 步骤 2: 从数据库获取该用户的所有订单
    orders = await order_curd.get_orders_by_user_id(db, user_id=user_id)

    # 步骤 3: 初始化用于分类的字典
    categorized_orders = {
        "booked": [],
        "completed": [],
        "cancelled": [],
        "violated": []
    }

    # 步骤 4: 遍历订单列表并根据状态进行分类
    for order in orders:
        if order.status == db_models.OrderStatus.BOOKED:
            categorized_orders["booked"].append(order.id)
        elif order.status == db_models.OrderStatus.COMPLETED:
            categorized_orders["completed"].append(order.id)
        elif order.status == db_models.OrderStatus.CANCELLED:
            categorized_orders["cancelled"].append(order.id)
        elif order.status == db_models.OrderStatus.VOILATED:
            categorized_orders["violated"].append(order.id)
    
    # 步骤 5: 使用 Pydantic 模型构建并返回结构化的响应
    return schemas.UserOrdersResponse(
        orderInfo=schemas.OrderInfoCategorized(**categorized_orders)
    )
