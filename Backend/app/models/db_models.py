from sqlalchemy import Column, String, Integer
from app.database.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = 
    nickname = Column(String(50))
    avatar = Column(String(255))
    
class Route(Base):
    __tablename__ = "routes"
    
    id = Column(String(50), primary_key=True, index=True, comment='路线ID')
    start_location = Column(String(100), nullable=False, comment='起点位置')
    end_location = Column(String(100), nullable=False, comment='终点位置')
    
    
class Bus(Base):
    __tablename__ = "buses"
    
    id = Column(String(50), primary_key=True, index=True, comment='班车ID')
    bus_number = Column(String(20), nullable=False, unique=True, index=True, comment='班车编号')
    capacity = Column(Integer, nullable=False, default=0, comment='座位数')
    route_id = Column(String(50), nullable=False, comment='路线ID')


# 订单
class order(Base):
    __tablename__ = "bus_orders"
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'comment': '班车订单主表',
        # 复合索引
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_date_status', 'departure_date', 'status'),
        Index('idx_route_bus', 'route_id', 'bus_id'),
    }
    id = Column(String(50), primary_key=True, index=True, comment='订单ID')
    order_no = Column(String(32), nullable=False, unique=True, index=True, comment='订单号')
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False, index=True, comment='用户ID')
    
    # 班车信息
    route_id = Column(String(50), ForeignKey('bus_routes.id'), nullable=False, comment='路线ID')
    bus_id = Column(String(50), ForeignKey('buses.id'), nullable=False, comment='班车ID')
    
    # 订单状态
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True, comment='订单状态')
    
    