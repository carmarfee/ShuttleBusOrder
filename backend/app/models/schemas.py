# app/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.db_models import OrderStatus
from datetime import datetime, time,date
# Pydantic模型用于请求和响应


# ===============================================================
# 令牌相关的模型 
# ===============================================================

class Token(BaseModel):
    """
    定义JWT令牌的响应格式。
    """
    access_token: str
    token_type: str




# ===============================================================
# 用户相关的模型 
# ===============================================================


class UserCreate(BaseModel):
    id: str = Field(..., description="用户ID，学工号")
    password: str = Field(..., min_length=1, max_length=50, description="用户密码")
    name: str = Field(..., min_length=1, max_length=50, description="用户名称")
    phone: str = Field(..., min_length=1, max_length=20, description="手机号码")
    role: str = Field(..., min_length=1, max_length=20, description="用户角色")
    department: Optional[str] = Field(None, max_length=50, description="部门")

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=50, description="用户密码")
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    role: Optional[str] = Field(None, min_length=1, max_length=20)
    department: Optional[str] = Field(None, max_length=50)

class UserResponse(BaseModel):
    id: str
    name: str
    #phone: str
    role: str
    department: Optional[str]
    
    class Config:
        from_attributes = True

class UserCreateByAdmin(BaseModel):
    """
    定义管理员添加新用户时使用的请求体格式。
    """
    id: str = Field(..., description="用户ID，学工号")
    name: str = Field(..., description="用户名称")
    password: str = Field(..., min_length=6, description="用户初始密码")
    phone: str = Field(..., description="手机号码 (必需)")
    role: str = Field(..., description="用户角色 (e.g., student, teacher, admin)")
    department: Optional[str] = Field(None, description="部门")


# ===============================================================
# auth/login
# ===============================================================

class LoginRequest(BaseModel):
    """
    定义登录接口的请求体格式 (简化版)。
    """
    id: str = Field(..., description="用户ID，学工号")
    password: str = Field(..., description="用户密码")
    role: str = Field(..., description="用户角色")


class LoginResponse(BaseModel):
    """
    定义登录成功后的响应格式 (保持不变)。
    """
    token: str
    userinfo: "UserResponse"


# 更新 LoginResponse 的模型引用
LoginResponse.update_forward_refs(UserResponse=UserResponse)


# ===============================================================
# 预约信息相关的模型 (新增部分)
# ===============================================================

class AppointmentInfoResponse(BaseModel):
    """
    定义获取预约信息接口的响应格式。
    """
    # 订单基本信息
    id: str
    order_no: str
    status: OrderStatus
    
    # 关联的用户信息
    user_id: str
    user_name: str
    
    # 关联的班次和路线信息
    route_id: str
    bus_id: str
    schedule_id: str
    
    # 衍生的信用情况
    credit_status: str = Field(..., description="根据订单状态衍生的信用情况")
    
    # 你可以根据需要添加更多字段，例如：
    # start_location: str
    # end_location: str
    # departure_time: datetime

# ===============================================================
# order
# ===============================================================

class RouteDetail(BaseModel):
    """用于表示路线详情的内嵌模型"""
    from_location: str = Field(..., alias='from')
    to_location: str = Field(..., alias='to')

class OrderDetailResponse(BaseModel):
    """
    定义获取单个订单详情接口的响应格式
    """
    route: RouteDetail
    bookedTime: datetime
    departureTime: time
    vehicleNumber: str
    state: str

    class Config:
        # 允许 Pydantic 使用别名 (例如 'from' 和 'to')
        allow_population_by_field_name = True

# ===============================================================
# order list
# ===============================================================

class OrderInfoCategorized(BaseModel):
    """
    用于内嵌在响应中，按状态分类存储订单ID列表。
    """
    booked: List[str] = []
    completed: List[str] = []
    cancelled: List[str] = [] # 注意：我已将你请求中的 "cancled" 修正为 "cancelled" 以匹配枚举
    violated: List[str] = []  # 注意：我已将你请求中的 "voilated" 修正为 "violated" 以匹配枚举

class UserOrdersResponse(BaseModel):
    """
    定义获取用户所有订单接口的响应格式。
    """
    orderInfo: OrderInfoCategorized

# ===============================================================
# 班次查询相关的模型 (新增部分)
# ===============================================================

class CapacityInfo(BaseModel):
    """用于表示座位容量信息"""
    booked: int
    total: int

class RouteInfo(BaseModel):
    """用于表示路线起止点"""
    # 使用别名，因为 'from' 是 Python 的保留关键字
    from_location: str = Field(..., alias='from')
    to_location: str = Field(..., alias='to')
    class Config:
        allow_population_by_field_name = True

class DriverInfo(BaseModel):
    """用于表示司机信息"""
    name: str = Field(..., alias='account') # 别名匹配输出格式
    phone: str
    class Config:
        allow_population_by_field_name = True

class BusServiceResponse(BaseModel):
    """
    定义查询班次接口中，单个班次信息的响应格式
    """
    departureTime: time
    vehicleNumber: str
    capacity: CapacityInfo
    route: RouteInfo
    driverInfo: DriverInfo
    schedule_id: str = Field(..., alias='schedule') # 别名匹配输出格式

    class Config:
        allow_population_by_field_name = True

# ===============================================================
# 动态通知相关的模型 
# ===============================================================

class DynamicItem(BaseModel):
    """
    定义动态通知列表中的单个项目。
    """
    id: str
    title: str
    time: datetime # FastAPI 会自动将 datetime 对象序列化为 ISO 8601 格式的字符串

class DynamicsResponse(BaseModel):
    """
    定义获取动态通知接口的响应格式。
    """
    dynamics: List[DynamicItem]

class DynamicContentResponse(BaseModel):
    """
    定义获取单条动态通知详细内容的响应格式。
    """
    id: str
    title: str
    publish_time: datetime
    content: str
    attachment_name: str
    attachment_url: Optional[str] = None # 附件URL可能为空

    class Config:
        # 这个配置允许 Pydantic 从 SQLAlchemy 的 ORM 对象自动转换数据
        from_attributes = True

# ===============================================================
# 路线相关的模型 (新增部分)
# ===============================================================

class RouteItem(BaseModel):
    """
    定义路线列表中的单个项目。
    """
    id: str
    # 使用别名 'from' 和 'to' 以匹配期望的输出格式
    from_location: str = Field(..., alias='from')
    to_location: str = Field(..., alias='to')
    
    class Config:
        allow_population_by_field_name = True


class RoutesResponse(BaseModel):
    """
    定义获取所有路线接口的响应格式。
    """
    routes: List[RouteItem]

# ===============================================================
# 预约相关的模型 (新增部分)
# ===============================================================

class AppointmentRequest(BaseModel):
    """
    定义预约接口的请求体格式。
    """
    user_id: str = Field(..., description="发起预约的用户的ID")
    schedule_id: str = Field(..., description="要预约的班次的ID")
    booking_date: date = Field(..., description="预约的乘车日期，格式为 YYYY-MM-DD")
    role: str = Field(..., description="预约人身份")

# ===============================================================
# 存储 OpenID 相关的模型 
# ===============================================================

class StoreOpenIDRequest(BaseModel):
    """
    定义存储 OpenID 接口的请求体格式。
    """
    id: str = Field(..., description="用户ID ")
    openid: str = Field(..., description="从微信获取的用户唯一标识 OpenID")






# ===============================================================
# 用户列表相关的模型 (新增部分)
# ===============================================================

class UserListItem(BaseModel):
    """定义用户列表中的单个用户信息"""
    id: str
    name: str
    role: str
    department: Optional[str]

class UserListResponse(BaseModel):
    """定义获取用户列表接口的响应格式"""
    userList: List[UserListItem]


# ===============================================================
# 班次列表相关的模型 (新增部分)
# ===============================================================

class RouteInfoForList(BaseModel):
    """用于表示路线起止点的内嵌模型"""
    from_location: str = Field(..., alias='from')
    to_location: str = Field(..., alias='to')
    
    class Config:
        allow_population_by_field_name = True

class ScheduleListItem(BaseModel):
    """定义班次列表中的单个班次信息"""
    vehicleNumber: str
    route: RouteInfoForList
    driver: str
    capacity: int # 返回为整数类型更佳
    scheduleID: str
    departureTime: time
    recurring_pattern: str

class ScheduleListResponse(BaseModel):
    """定义获取班次列表接口的响应格式"""
    scheduleList: List[ScheduleListItem]

# ===============================================================
# 添加班次相关的模型 (新增部分)
# ===============================================================

class ScheduleCreateRequest(BaseModel):
    """
    定义添加新班次接口的请求体格式。
    使用了别名来匹配前端发送的字段名。
    """
    vehicleNumber: str
    route_id: str = Field(..., alias="route")
    driver_name: str = Field(..., alias="driver")
    capacity: int # FastAPI会自动将字符串数字转换为整数
    scheduleID: str
    departureTime: time
    # 以下字段对于创建班次是必需的，但未在您的输入列表中，我已添加为可选
    # 您可以根据需要将它们改为必需，或在API层提供默认值
    recurring_pattern: Optional[str] = "周一到周五"
    departure_location: Optional[str] = "主校区"
    arrival_location: Optional[str] = "新校区"
    
    class Config:
        allow_population_by_field_name = True

class ScheduleCreateResponse(BaseModel):
    """
    定义添加新班次成功后的响应格式。
    """
    bus_id: str
    schedule_id: str
    message: str = "班车及班次已成功添加"





