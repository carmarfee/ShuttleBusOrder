from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Text, Boolean,
    Date, Time, Enum, JSON, Index, BIGINT
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
    BOOKED = "booked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    VOILATED = "violated"
    

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
    name = Column(String(50), index=True, nullable=False)
    password = Column(String(50), index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    role = Column(String(20), nullable=False, index=True)
    department = Column(String(50), nullable=True, index=True)
    
    # 添加关系
    orders = relationship("Order", back_populates="user")


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
    
    # 添加关系
    orders = relationship("Order", back_populates="route")
    
    
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
    
    # 添加关系
    schedules = relationship("BusSchedule", back_populates="bus")
    orders = relationship("Order", back_populates="bus")


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
    booking_date = Column(Date, nullable=False, index=True, comment='预约发车日期')
    
    # 订单状态
    status = Column(Enum(OrderStatus), default=OrderStatus.BOOKED, index=True, comment='订单状态')

    #订单时间
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, comment='预约时间')
    
    # 关系
    user = relationship("User", back_populates="orders")
    route = relationship("Route", back_populates="orders")
    bus = relationship("Bus", back_populates="orders")
    schedule = relationship("BusSchedule", back_populates="orders")


# 动态通知
class Dynamics(Base):
    __tablename__ = "dynamics"
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '动态通知',
    }
    id = Column(String(50), primary_key=True, index=True, comment='动态ID')
    title = Column(String(200), nullable=False, comment='标题')
    publish_time = Column(DateTime, nullable=False, index=True, comment='发布时间')
    content = Column(Text, nullable=False, comment='内容')
    attachment_name = Column(String(200), nullable=False, comment='文件名')
    attachment_url = Column(String(500), comment='文件访问URL')



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