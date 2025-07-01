# app/api/endpoints/appointment.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta

from app.models.db_models import get_db
from app.models import schemas, db_models
from app.services import order_curd, schedule_curd, user_curd # 假设user_curd里有 get_user
from app.core.auth import get_current_user
from app.core.config import settings 
from app.services.schedule_curd import is_date_in_pattern 

router = APIRouter()

# 定义违约次数上限
MAX_VIOLATION_COUNT = 3

@router.post(
    "/appointment",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="创建新的班车预约"
)
async def create_appointment(
    *,
    db: AsyncSession = Depends(get_db),
    appointment_req: schemas.AppointmentRequest,
    # current_user: db_models.User = Depends(get_current_user)
):
    """
    为当前登录用户创建一个新的班车预约。
    执行多项业务规则校验：
    - 权限：用户只能为自己预约。
    - 违约次数：检查用户是否因多次违约被限制。
    - 班次有效性：检查班次是否存在且在预约日期运营。
    - 重复预订：检查用户是否已预订过同一天的同一班次。
    - 座位容量：检查班次是否还有余座。
    - 优先级校验，老师能有额外的预约能力
    """
    # 1. 权限校验：用户只能为自己预约
    # if current_user.id != appointment_req.user_id:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, "不能为其他用户创建预约。")

    # 2. 违约次数检查
    violation_count = await order_curd.count_violated_orders_by_user_id(db, user_id=appointment_req.user_id)
    if violation_count >= MAX_VIOLATION_COUNT:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"因违约次数达到{violation_count}次，您已被暂时限制预约。")

    # 3. 班次有效性检查
    schedule = await schedule_curd.get_schedule_by_id_with_bus(db, schedule_id=appointment_req.schedule_id)
    if not schedule:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "指定的班次不存在。")
        
    if not is_date_in_pattern(appointment_req.booking_date, schedule.recurring_pattern):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "该班次在指定日期不运营。")

    # 4. 【新】预约时间窗口检查
    today = date.today()
    booking_window_days = 0
    if appointment_req.role == settings.TEACHER_ROLE_NAME:
        booking_window_days = settings.TEACHER_BOOKING_WINDOW_DAYS
    elif appointment_req.role == settings.STUDENT_ROLE_NAME:
        booking_window_days = settings.STUDENT_BOOKING_WINDOW_DAYS
    # (可以为其他角色添加更多 else if)

    latest_allowed_date = today + timedelta(days=booking_window_days)
    
    if appointment_req.booking_date < today:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "不能预约过去的日期。")
    if appointment_req.booking_date > latest_allowed_date:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"预约失败，您只能提前 {booking_window_days} 天进行预约。")

    # 5. 重复预订检查
    existing_order = await order_curd.get_user_order_for_schedule_on_date(
        db, 
        user_id=appointment_req.id, 
        schedule_id=appointment_req.schedule_id, 
        booking_date=appointment_req.booking_date
    )
    if existing_order:
        raise HTTPException(status.HTTP_409_CONFLICT, "您已预订过该日期的同一班次。")

    # 6. 【新】座位容量与优先级检查
    bus_capacity = schedule.bus.capacity
    booked_seats = await order_curd.count_booked_seats_for_schedule_on_date(
        db, 
        schedule_id=appointment_req.schedule_id, 
        booking_date=appointment_req.booking_date
    )
    
    # 首先，检查是否已完全满座
    if booked_seats >= bus_capacity:
        raise HTTPException(status.HTTP_409_CONFLICT, "该班次座位已满。")

    # 其次，如果用户不是老师，则检查是否已达到普通座位的上限
    if appointment_req.role != settings.TEACHER_ROLE_NAME:
        general_seats_limit = bus_capacity - settings.TEACHER_RESERVED_SEATS
        if booked_seats >= general_seats_limit:
            raise HTTPException(status.HTTP_409_CONFLICT, "该班次普通座位已满，剩余座位为教师预留。")

    # 7. 所有检查通过，创建订单
    await order_curd.create_order(db, appointment_req=appointment_req)

    # 成功，返回 204 No Content
    return Response(status_code=status.HTTP_204_NO_CONTENT)