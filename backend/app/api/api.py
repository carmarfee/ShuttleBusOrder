from fastapi import APIRouter
from app.api.endpoints import login,get_orderinfo,get_orders,search_busservices,get_dynamics,get_dynamiccontent,get_creditinfo,get_routes,appointment,send_notification
api_router = APIRouter()

api_router.include_router(login.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(get_orderinfo.router, tags=["获取order单个信息"])
api_router.include_router(get_orders.router, tags=["获取用户所有order"])
api_router.include_router(search_busservices.router, tags=["查询某条路线某个日期的活动班次"])
api_router.include_router(get_dynamics.router, tags=["获取最新的三条通知"])
api_router.include_router(get_dynamiccontent.router, tags=["获取一条通知的详细信息"])
api_router.include_router(get_creditinfo.router, tags=["获取违约次数"])
api_router.include_router(get_routes.router, tags=["获取路线信息"])
api_router.include_router(appointment.router, tags=["预约"])
api_router.include_router(send_notification.router, tags=["推送消息测试API"])