# app/api/endpoints/search_busservices.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import List

from app.models.db_models import get_db
from app.models import schemas
from app.services import schedule_curd

router = APIRouter()

@router.get(
    "/searchBusServices",
    response_model=List[schemas.BusServiceResponse],
    summary="查询某条路线在特定日期的所有班次"
)
async def search_bus_services(
    *,
    db: AsyncSession = Depends(get_db),
    route_id: str = Query(..., alias="route", description="路线的唯一ID"),
    booking_date_str: str = Query(..., alias="time", description="查询日期，格式为 YYYY-MM-DD")
):
    """
    根据路线ID和日期，查询所有符合条件的班车服务信息。
    """
    try:
        # 将日期字符串转换为 date 对象
        target_date = date.fromisoformat(booking_date_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="日期格式无效，请使用 YYYY-MM-DD 格式。"
        )

    # 调用服务函数获取数据
    active_schedules = await schedule_curd.find_active_schedules(
        db, route_id=route_id, target_date=target_date
    )

    # 将查询结果转换为 API 响应格式
    response_list = []
    for item in active_schedules:
        schedule = item["schedule"]
        bus = item["bus"]
        route = item["route"]
        booked_seats = item["booked_seats"]
        
        service_response = schemas.BusServiceResponse(
            departureTime=schedule.departure_time,
            vehicleNumber=bus.bus_number,
            capacity=schemas.CapacityInfo(
                booked=booked_seats,
                total=bus.capacity
            ),
            route=schemas.RouteInfo(
                from_location=route.start_location,
                to_location=route.end_location
            ),
            driverInfo=schemas.DriverInfo(
                name=bus.driver_name,
                phone=bus.driver_phone
            ),
            schedule_id=schedule.id
        )
        response_list.append(service_response)

    return response_list

