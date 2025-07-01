# app/services/route_crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models import db_models

async def get_all_routes(db: AsyncSession) -> List[db_models.Route]:
    """
    从数据库中异步获取所有的路线记录。

    Args:
        db: 数据库会话。

    Returns:
        一个包含 Route SQLAlchemy 对象的列表。
    """
    # 创建一个查询，选择所有的路线
    query = select(db_models.Route)
    
    # 执行查询
    result = await db.execute(query)
    
    # 返回所有匹配的记录
    return result.scalars().all()


async def get_route_by_id(db: AsyncSession, route_id: str) -> Optional[db_models.Route]:
    """根据ID获取单个路线。"""
    return await db.get(db_models.Route, route_id)

