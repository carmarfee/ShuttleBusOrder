# app/api/endpoints/add_schedule.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import get_db
from app.models import schemas, db_models
from app.services import bus_curd, route_curd, schedule_curd
from app.core.auth import get_current_admin_user

router = APIRouter()

@router.post(
    "/addSchedule",
    status_code=status.HTTP_200_OK,
    summary="管理员添加新的班车和班次"
)
async def add_schedule(
    *,
    db: AsyncSession = Depends(get_db),
    schedule_in: schemas.ScheduleCreateRequest,
    admin_user: db_models.User = Depends(get_current_admin_user)
):
    """
    由管理员创建一个新的班车及其初始班次。
    - **需要管理员权限。**
    - 会检查路线是否存在和车牌号是否重复。
    """
    # 1. 验证路线是否存在
    route = await route_curd.get_route_by_id(db, route_id=schedule_in.route_id)
    if not route:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"ID为 '{schedule_in.route_id}' 的路线不存在。")

    # 2. 验证车牌号是否已存在
    existing_bus = await bus_curd.get_bus_by_number(db, bus_number=schedule_in.vehicleNumber)
    if existing_bus:
        raise HTTPException(status.HTTP_409_CONFLICT, f"车牌号为 '{schedule_in.vehicleNumber}' 的巴士已存在。")

    # 3. 创建新的巴士和班次对象
    # 注意：这里我们还没有 commit 到数据库
    new_bus = await bus_curd.create_bus(db, bus_data=schedule_in)
    new_schedule = await schedule_curd.create_schedule(db, schedule_data=schedule_in, bus_id=new_bus.id)

    # 4. 一次性提交所有更改到数据库
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"数据库操作失败: {e}")

    return 
