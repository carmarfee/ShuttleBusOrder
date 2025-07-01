# app/api/endpoints/list_apis.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# 请根据你的项目结构调整 import 路径
from app.models.db_models import get_db
from app.models import schemas, db_models
from app.services import user_curd, schedule_curd
from app.core.auth import get_current_admin_user

router = APIRouter()

@router.get(
    "/getUserList",
    response_model=schemas.UserListResponse,
    summary="管理员获取用户列表"
)
async def get_user_list(
    *,
    db: AsyncSession = Depends(get_db),
    # 使用分页参数
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=200, description="返回的记录数上限"),
    # 依赖管理员认证
    admin_user: db_models.User = Depends(get_current_admin_user)
):
    """
    获取系统中的用户列表，支持分页。
    - **需要管理员权限。**
    """
    db_users = await user_curd.get_all_users(db, skip=skip, limit=limit)
    
    # 将数据库对象转换为 Pydantic 模型
    user_list_items = [
        schemas.UserListItem(
            id=user.id,
            name=user.name,
            role=user.role,
            department=user.department
        ) for user in db_users
    ]
    
    return schemas.UserListResponse(userList=user_list_items)


@router.get(
    "/getScheduleList",
    response_model=schemas.ScheduleListResponse,
    summary="获取所有班次列表"
)
async def get_schedule_list(
    db: AsyncSession = Depends(get_db)
):
    """
    获取系统中所有已定义的班车班次列表及其详细信息。
    - **此接口为公开接口，无需认证。**
    """
    # 从服务层获取包含 (Schedule, Bus, Route) 元组的列表
    schedules_with_details = await schedule_curd.get_all_schedules_with_details(db)
    
    # 将查询结果转换为 API 响应格式
    schedule_list_items = []
    for schedule, bus, route in schedules_with_details:
        item = schemas.ScheduleListItem(
            vehicleNumber=bus.bus_number,
            route=schemas.RouteInfoForList(
                from_location=route.start_location,
                to_location=route.end_location
            ),
            driver=bus.driver_name,
            capacity=bus.capacity,
            scheduleID=schedule.id,
            departureTime=schedule.departure_time,
            recurring_pattern=schedule.recurring_pattern
        )
        schedule_list_items.append(item)
        
    return schemas.ScheduleListResponse(scheduleList=schedule_list_items)
