# app/api/endpoints/get_dynamics.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# 请根据你的项目结构调整 import 路径
from app.models.db_models import get_db
from app.models import schemas
from app.services import dynamics_curd

router = APIRouter()

@router.get(
    "/getDynamics",
    response_model=schemas.DynamicsResponse,
    summary="获取最新的三条动态通知"
)
async def get_latest_dynamics_api(
    db: AsyncSession = Depends(get_db)
    # current_user: db_models.User = Depends(get_current_user)
):
    """
    获取系统中最新的三条动态通知。
    此接口为公开接口，无需认证即可访问。
    """
    # 步骤 1: 调用服务函数获取数据库记录
    latest_dynamics_from_db = await dynamics_curd.get_latest_dynamics(db, limit=3)

    # 步骤 2: 将数据库对象列表转换为 Pydantic 模型列表
    # 我们手动构建列表，以确保字段名称正确映射 (db: publish_time -> response: time)
    response_items = [
        schemas.DynamicItem(
            id=dynamic.id,
            title=dynamic.title,
            time=dynamic.publish_time 
        )
        for dynamic in latest_dynamics_from_db
    ]
    
    # 步骤 3: 使用 Pydantic 模型构建并返回最终的响应
    return schemas.DynamicsResponse(dynamics=response_items)
