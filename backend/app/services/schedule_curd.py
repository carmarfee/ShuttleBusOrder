# app/services/schedule_crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from datetime import date
from typing import List, Any, Optional
from sqlalchemy.orm import joinedload
from app.models import db_models ,schemas

def is_date_in_pattern(target_date: date, pattern: str) -> bool:
    """
    检查给定日期是否符合发车周期的辅助函数。
    这是一个简化的实现，你可以根据需要扩展它。
    """
    weekday = target_date.weekday() # Monday is 0 and Sunday is 6
    
    # 简单的模式匹配
    if pattern == "周一到周五" and 0 <= weekday <= 4:
        return True
    if pattern == "周一到周日" and 0 <= weekday <= 6:
        return True
    if pattern == "周末" and 5 <= weekday <= 6:
        return True
        
    # 你可以添加更多模式，例如 "单双号" 等
    
    return False


async def find_active_schedules(
    db: AsyncSession, *, route_id: str, target_date: date
) -> List[Any]:
    """
    查询在指定路线和日期下所有活跃的班次信息。
    """
    
    # 1. 创建一个子查询，用于计算每个班次在指定日期的已预订座位数
    booked_seats_subquery = (
        select(
            db_models.Order.schedule_id,
            func.count(db_models.Order.id).label("booked_count")
        )
        .where(
            db_models.Order.booking_date == target_date,
            # 只计算有效预订（非取消或违约）
            db_models.Order.status.in_([db_models.OrderStatus.BOOKED, db_models.OrderStatus.COMPLETED])
        )
        .group_by(db_models.Order.schedule_id)
        .subquery()
    )

    # 2. 创建主查询
    query = (
        select(
            db_models.BusSchedule,
            db_models.Bus,
            db_models.Route,
            # 使用 Coalesce 函数处理没有预订记录的情况，默认为0
            func.coalesce(booked_seats_subquery.c.booked_count, 0).label("booked_seats")
        )
        # 关联各个表
        .join(db_models.Bus, db_models.BusSchedule.bus_id == db_models.Bus.id)
        .join(db_models.Route, db_models.Bus.route_id == db_models.Route.id)
        # 使用 left join，确保即使班次无人预订也能被查出来
        .outerjoin(booked_seats_subquery, db_models.BusSchedule.id == booked_seats_subquery.c.schedule_id)
        # 筛选条件：路线ID匹配
        .where(db_models.Route.id == route_id)
    )

    # 执行查询，获取所有潜在的班次
    all_schedules_on_route = await db.execute(query)
    results = all_schedules_on_route.all()
    
    # 3. 在 Python 中进行日期模式的过滤
    # 因为 recurring_pattern 的逻辑比较复杂，在代码中处理比在SQL中更灵活
    active_schedules = []
    for schedule, bus, route, booked_seats in results:
        if is_date_in_pattern(target_date, schedule.recurring_pattern):
            # 将所有需要的信息打包在一起
            active_schedules.append({
                "schedule": schedule,
                "bus": bus,
                "route": route,
                "booked_seats": booked_seats
            })
            
    return active_schedules


async def get_schedule_by_id_with_bus(
    db: AsyncSession, schedule_id: str
) -> Optional[db_models.BusSchedule]:
    """根据ID获取班次，并预加载关联的车辆信息。"""
    query = (
        select(db_models.BusSchedule)
        .options(joinedload(db_models.BusSchedule.bus))
        .filter(db_models.BusSchedule.id == schedule_id)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_schedules_with_details(db: AsyncSession) -> List[Any]:
    """
    异步获取所有班次及其关联的车辆和路线信息。
    """
    query = (
        select(
            db_models.BusSchedule,
            db_models.Bus,
            db_models.Route
        )
        # 使用 JOIN 将三个表关联起来
        .join(db_models.Bus, db_models.BusSchedule.bus_id == db_models.Bus.id)
        .join(db_models.Route, db_models.Bus.route_id == db_models.Route.id)
        .order_by(db_models.BusSchedule.departure_time) # 按发车时间排序
    )
    result = await db.execute(query)
    # .all() 会返回一个元组(tuple)的列表，每个元组包含 (Schedule, Bus, Route) 对象
    return result.all()


async def create_schedule(db: AsyncSession, *, schedule_data: schemas.ScheduleCreateRequest, bus_id: str) -> db_models.BusSchedule:
    """创建一个新的班次记录。"""
    new_schedule = db_models.BusSchedule(
        id=schedule_data.scheduleID,
        bus_id=bus_id,
        departure_time=schedule_data.departureTime,
        recurring_pattern=schedule_data.recurring_pattern,
        departure_location=schedule_data.departure_location,
        arrival_location=schedule_data.arrival_location
    )
    db.add(new_schedule)
    # 我们将在上层调用中一起 commit
    return new_schedule