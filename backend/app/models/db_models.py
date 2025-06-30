from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Text, Boolean,
    Date, Time, Enum, JSON, Index, BIGINT, Decimal
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import os
import enum

# MySQL数据库URL配置
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
)

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 开发环境下显示SQL语句
    future=True,
    pool_size=20,  # 连接池大小
    max_overflow=30,  # 最大溢出连接数
    pool_timeout=30,  # 获取连接超时时间
    pool_recycle=3600,  # 连接回收时间（1小时）
    pool_pre_ping=True,  # 连接前ping检查，处理MySQL连接超时
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# 添加缺失的枚举定义
class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

# 模型定义
class User(Base):
    __tablename__ = "users"
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '用户表'
        
    }
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(50), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    role = Column(String(20), nullable=False, index=True)
    department = Column(String(50), nullable=True, index=True)


class Route(Base):
    __tablename__ = "routes"
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '班车路线表'
    }
    
    id = Column(String(50), primary_key=True, index=True, comment='路线ID')
    start_location = Column(String(100), nullable=False, comment='起点位置')
    end_location = Column(String(100), nullable=False, comment='终点位置')
    
    
class Bus(Base):
    __tablename__ = "buses"
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '班车表'
    }
    
    id = Column(String(50), primary_key=True, index=True, comment='班车ID')
    bus_number = Column(String(20), nullable=False, unique=True, index=True, comment='班车编号')
    driver_name = Column(String(50), comment='司机姓名')
    driver_phone = Column(String(20), comment='司机电话')
    capacity = Column(Integer, nullable=False, default=0, comment='座位数')
    route_id = Column(String(50), nullable=False, comment='路线ID')


class BusSchedule(Base):
    __tablename__ = "schedule"
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '班车时刻表',
    }
    
    id = Column(String(50), primary_key=True, index=True, comment='时刻表ID')
    bus_id = Column(String(50), ForeignKey('buses.id'), nullable=False, comment='班车ID')
    departure_time = Column(Time, nullable=False, comment='发车时间')
    
    # 例如图片中的"周一到周五"、"周一到周日"
    recurring_pattern = Column(String(50), comment='发车周期，如：周一到周五、周一到周日')
    
    # 根据图片信息，添加更详细的位置信息
    departure_location = Column(String(100), comment='具体发车地点，如：信息学部国重门口')
    arrival_location = Column(String(100), comment='具体到达地点，如：新校区新珈楼')

    # 关系
    bus = relationship("Bus", back_populates="schedules")
    orders = relationship("Order", back_populates="schedule")

# 订单
class Order(Base):
    __tablename__ = "bus_orders"
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '班车订单主表',
    }
    id = Column(String(50), primary_key=True, index=True, comment='订单ID')
    order_no = Column(String(32), nullable=False, unique=True, index=True, comment='订单号')
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False, index=True, comment='用户ID')
    
    # 班车信息
    route_id = Column(String(50), ForeignKey('routes.id'), nullable=False, comment='路线ID')
    bus_id = Column(String(50), ForeignKey('buses.id'), nullable=False, comment='班车ID')
    schedule_id = Column(String(50), ForeignKey('schedule.id'), nullable=False, comment='班次ID')
    
    # 订单状态
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True, comment='订单状态')
    
    # 关系
    schedule = relationship("BusSchedule", back_populates="orders")


# 在Bus类中添加关系
Bus.schedules = relationship("BusSchedule", back_populates="bus")

# 动态通知



# 异步数据库会话依赖
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# 创建表的异步函数
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)