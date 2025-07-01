# app/services/dynamics_crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models import db_models

async def get_latest_dynamics(db: AsyncSession, limit: int = 3) -> List[db_models.Dynamics]:
    """
    从数据库中异步获取最新的动态通知记录。

    Args:
        db: 数据库会话。
        limit: 要获取的记录数量，默认为3。

    Returns:
        一个包含 Dynamics SQLAlchemy 对象的列表。
    """
    # 创建一个查询，选择 Dynamics 表
    query = (
        select(db_models.Dynamics)
        # 按发布时间降序排序，以获取最新的记录
        .order_by(db_models.Dynamics.publish_time.desc())
        # 限制返回的记录数量
        .limit(limit)
    )
    
    # 执行查询
    result = await db.execute(query)
    
    # 返回所有匹配的记录
    return result.scalars().all()


async def get_dynamic_by_id(db: AsyncSession, dynamic_id: str) -> Optional[db_models.Dynamics]:
    """
    根据ID异步获取单个动态通知。

    Args:
        db: 数据库会话。
        dynamic_id: 要查询的动态通知的ID。

    Returns:
        一个 Dynamics SQLAlchemy 对象，如果不存在则返回 None。
    """
    # 创建一个查询，选择 ID 匹配的单个记录
    query = select(db_models.Dynamics).filter(db_models.Dynamics.id == dynamic_id)
    
    # 执行查询
    result = await db.execute(query)
    
    # 使用 .scalar_one_or_none() 安全地获取单个结果
    return result.scalar_one_or_none()
