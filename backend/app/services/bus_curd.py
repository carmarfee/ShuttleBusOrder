# app/services/bus_curd.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import uuid

from app.models import db_models, schemas

async def get_bus_by_number(db: AsyncSession, bus_number: str) -> Optional[db_models.Bus]:
    """根据车牌号查询巴士。"""
    query = select(db_models.Bus).filter(db_models.Bus.bus_number == bus_number)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_bus(db: AsyncSession, *, bus_data: schemas.ScheduleCreateRequest) -> db_models.Bus:
    """创建一个新的巴士记录。"""
    new_bus = db_models.Bus(
        id=f"bus_{bus_data.vehicleNumber.lower()}_{uuid.uuid4().hex[:4]}",
        bus_number=bus_data.vehicleNumber,
        driver_name=bus_data.driver_name,
        capacity=bus_data.capacity,
        route_id=bus_data.route_id,
        # 假设司机的电话号码与车牌号相同，或者您可以修改此逻辑
        driver_phone=bus_data.vehicleNumber 
    )
    db.add(new_bus)
    # 我们将在上层调用中一起 commit
    return new_bus
