# app/api/endpoints/get_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# 请根据你的项目结构调整 import 路径
from app.models.db_models import get_db
from app.models import schemas
from app.services import route_curd

router = APIRouter()

@router.get(
    "/getRoutes",
    response_model=schemas.RoutesResponse,
    summary="获取所有班车路线"
)
async def get_all_routes_api(
    db: AsyncSession = Depends(get_db)
):
    """
    获取系统中所有已定义的班车路线列表。
    此接口为公开接口，无需认证即可访问。
    """
    # 步骤 1: 调用服务函数获取所有路线的数据库记录
    db_routes = await route_curd.get_all_routes(db)
    
    # 步骤 2: 将数据库对象列表转换为 Pydantic 模型列表
    # 这一步是必要的，因为我们的 Pydantic 模型使用了别名
    route_items = [
        schemas.RouteItem(
            id=route.id,
            from_location=route.start_location,
            to_location=route.end_location
        ) 
        for route in db_routes
    ]

    # 步骤 3: 使用 Pydantic 模型构建并返回最终的响应
    return schemas.RoutesResponse(routes=route_items)
