import asyncio
from datetime import datetime, date, time
from decimal import Decimal
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import (  # 替换为你的模型文件名
    AsyncSessionLocal, User, Route, Bus, BusSchedule, Order, OrderStatus
)

async def insert_sample_data():
    """插入基于图片时刻表的示例数据"""
    async with AsyncSessionLocal() as session:
        try:
            # 1. 插入用户数据
            users_data = [
                {
                    "id": str(uuid.uuid4()),
                    "name": "张三",
                    "password": "123456",
                    "phone": "13800138001",
                    "role": "student",
                    "department": "计算机学院"
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "李四", 
                    "password": "123456"
                    "phone": "13800138002",
                    "role": "teacher",
                    "department": "信息学部"
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "王五",
                    "password": "123456"
                    "phone": "13800138003", 
                    "role": "driver",
                    "department": "行政部"
                }
            ]
            
            users = []
            for user_data in users_data:
                user = User(**user_data)
                users.append(user)
                session.add(user)
            
            # 2. 插入路线数据
            routes_data = [
                {
                    "id": "route_main_to_new",
                    "start_location": "本部",
                    "end_location": "新校区"
                },
                {
                    "id": "route_new_to_main", 
                    "start_location": "新校区",
                    "end_location": "本部"
                }
            ]
            
            routes = []
            for route_data in routes_data:
                route = Route(**route_data)
                routes.append(route)
                session.add(route)
            
            # 3. 插入班车数据（基于图片中的车辆信息）
            buses_data = [
                # 本部→新校区方向的班车
                {
                    "id": "bus_ayb260_1",
                    "bus_number": "AYB260",
                    "driver_name": "杨师傅", 
                    "driver_phone": "13971341207",
                    "capacity": 50,
                    "route_id": "route_main_to_new"
                },
                {
                    "id": "bus_alb328_1",
                    "bus_number": "ALB328",
                    "driver_name": "吴师傅",
                    "driver_phone": "15907179119", 
                    "capacity": 45,
                    "route_id": "route_main_to_new"
                },
                {
                    "id": "bus_alb160_1",
                    "bus_number": "ALB160",
                    "driver_name": "范师傅",
                    "driver_phone": "13349989991",
                    "capacity": 40,
                    "route_id": "route_main_to_new"
                },
                # 新校区→本部方向的班车
                {
                    "id": "bus_alb160_2",
                    "bus_number": "ALB160",
                    "driver_name": "范师傅",
                    "driver_phone": "13349989991", 
                    "capacity": 40,
                    "route_id": "route_new_to_main"
                },
                {
                    "id": "bus_ayb260_2",
                    "bus_number": "AYB260", 
                    "driver_name": "杨师傅",
                    "driver_phone": "13971341207",
                    "capacity": 50,
                    "route_id": "route_new_to_main"
                },
                {
                    "id": "bus_alb328_2",
                    "bus_number": "ALB328",
                    "driver_name": "吴师傅",
                    "driver_phone": "15907179119",
                    "capacity": 45, 
                    "route_id": "route_new_to_main"
                }
            ]
            
            buses = []
            for bus_data in buses_data:
                bus = Bus(**bus_data)
                buses.append(bus)
                session.add(bus)
            
            # 提交基础数据
            await session.commit()
            
            # 4. 插入班车时刻表数据（基于图片中的时刻表）
            schedules_data = [
                # 本部→新校区
                {
                    "id": str(uuid.uuid4()),
                    "bus_id": "bus_ayb260_1",
                    "schedule_date": date.today(),
                    "departure_time": time(7, 0),  # 07:00
                    "recurring_pattern": "周一到周五",
                    "departure_location": "信息学部国重门口",
                    "arrival_location": "新校区新驻楼",
                },
                {
                    "id": str(uuid.uuid4()),
                    "bus_id": "bus_alb328_1", 
                    "schedule_date": date.today(),
                    "departure_time": time(12, 40),  # 12:40
                    "recurring_pattern": "周一到周五",
                    "departure_location": "信息学部国重门口",
                    "arrival_location": "新校区新驻楼"
                },
                {
                    "id": str(uuid.uuid4()),
                    "bus_id": "bus_alb160_1",
                    "schedule_date": date.today(), 
                    "departure_time": time(19, 0),  # 19:00
                    "recurring_pattern": "周一到周日",
                    "departure_location": "本部当代楼校巴站",
                    "arrival_location": "新校区一食堂"
                },
                # 新校区→本部
                {
                    "id": str(uuid.uuid4()),
                    "bus_id": "bus_alb160_2",
                    "schedule_date": date.today(),
                    "departure_time": time(6, 40),  # 06:40
                    "recurring_pattern": "周一到周日", 
                    "departure_location": "新校区一食堂",
                    "arrival_location": "本部当代楼校巴站"
                },
                {
                    "id": str(uuid.uuid4()),
                    "bus_id": "bus_ayb260_2",
                    "schedule_date": date.today(),
                    "departure_time": time(12, 20),  # 12:20
                    "recurring_pattern": "周一到周五",
                    "departure_location": "新校区新驻楼",
                    "arrival_location": "本部当代楼校巴站"
                },
                {
                    "id": str(uuid.uuid4()),
                    "bus_id": "bus_alb328_2",
                    "schedule_date": date.today(),
                    "departure_time": time(17, 30),  # 17:30
                    "recurring_pattern": "周一到周五",
                    "departure_location": "新校区新驻楼", 
                    "arrival_location": "信息学部国重门口"
                }
            ]
            
            schedules = []
            for schedule_data in schedules_data:
                schedule = BusSchedule(**schedule_data)
                schedules.append(schedule)
                session.add(schedule)
            
            # 5. 插入示例订单数据
            orders_data = [
                {
                    "id": str(uuid.uuid4()),
                    "order_no": f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}001",
                    "user_id": users[0].id,
                    "route_id": "route_main_to_new",
                    "bus_id": "bus_ayb260_1", 
                    "schedule_id": schedules[0].id,
                    "status": OrderStatus.CONFIRMED
                },
                {
                    "id": str(uuid.uuid4()),
                    "order_no": f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}002",
                    "user_id": users[1].id,
                    "route_id": "route_new_to_main",
                    "bus_id": "bus_alb160_2",
                    "schedule_id": schedules[3].id,
                    "status": OrderStatus.PENDING
                }
            ]
            
            for order_data in orders_data:
                order = Order(**order_data)
                session.add(order)
            
            # 提交所有数据
            await session.commit()
            print("数据插入成功！")
            print(f"插入了 {len(users)} 个用户")
            print(f"插入了 {len(routes)} 条路线")
            print(f"插入了 {len(buses)} 辆班车")
            print(f"插入了 {len(schedules)} 个班次")
            print(f"插入了 {len(orders_data)} 个订单")
            
        except Exception as e:
            await session.rollback()
            print(f"数据插入失败: {e}")
            raise


async def clear_all_data():
    """清空所有表数据（谨慎使用）"""
    async with AsyncSessionLocal() as session:
        try:
            # 按照外键依赖关系的相反顺序删除
            await session.execute("DELETE FROM bus_orders")
            await session.execute("DELETE FROM schedule") 
            await session.execute("DELETE FROM buses")
            await session.execute("DELETE FROM routes")
            await session.execute("DELETE FROM users")
            await session.commit()
            print("所有数据已清空")
        except Exception as e:
            await session.rollback()
            print(f"清空数据失败: {e}")
            raise
