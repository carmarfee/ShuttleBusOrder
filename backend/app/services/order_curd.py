# app/services/order_crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select ,func
from sqlalchemy.orm import joinedload
from typing import List, Optional

from app.models import db_models

async def get_order_by_id(db: AsyncSession, order_id: str) -> Optional[db_models.Order]:
    """
    根据订单ID异步获取单个订单。

    为了获取所有需要的信息，我们使用 joinedload 一次性加载
    所有关联的表 (Route, Bus, BusSchedule)。
    这比多次查询数据库要高效得多。
    """
    query = (
        select(db_models.Order)
        .options(
            joinedload(db_models.Order.route),
            joinedload(db_models.Order.bus),
            joinedload(db_models.Order.schedule)
        )
        .filter(db_models.Order.id == order_id)
    )
    result = await db.execute(query)
    # scalar_one_or_none() 用于获取单个结果，如果不存在则返回 None
    return result.scalar_one_or_none()

async def get_orders_by_user_id(db: AsyncSession, user_id: str) -> List[db_models.Order]:
    """
    根据用户ID异步获取该用户的所有订单列表。
    """
    # 创建一个查询，选择所有 user_id 匹配的订单
    query = select(db_models.Order).filter(db_models.Order.user_id == user_id)
    
    # 执行查询
    result = await db.execute(query)
    
    # 返回所有匹配的订单对象列表
    return result.scalars().all()

async def count_violated_orders_by_user_id(db: AsyncSession, user_id: str) -> int:
    """
    计算给定用户的违约订单数量。
    """
    # 创建一个查询，计算 user_id 匹配且状态为 VOILATED 的订单数量
    query = (
        select(func.count(db_models.Order.id))
        .where(
            db_models.Order.user_id == user_id,
            db_models.Order.status == db_models.OrderStatus.VOILATED
        )
    )
    result = await db.execute(query)
    # scalar_one() 会返回第一行第一列的单个值，这里就是我们计算出的数量
    return result.scalar_one()
