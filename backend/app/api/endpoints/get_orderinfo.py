# app/api/endpoints/get_appointmentinfo.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# 请根据你的项目结构调整 import 路径
from app.models.db_models import get_db
from app.models import schemas, db_models
from app.services import order_curd # 导入新的 order_crud
from app.core.auth import get_current_user # 引入认证，确保只有登录用户能查询

router = APIRouter()

def map_order_status_to_state(order_status: db_models.OrderStatus) -> str:
    """
    将数据库中的订单状态枚举映射为人类可读的字符串。
    """
    status_map = {
        db_models.OrderStatus.COMPLETED: "已完成",
        db_models.OrderStatus.CANCELLED: "已取消",
        db_models.OrderStatus.VOILATED: "违约",
        db_models.OrderStatus.BOOKED: "已预约",
    }
    return status_map.get(order_status, "未知状态")


@router.get(
    "/getOrderDetail/{order_id}", 
    response_model=schemas.OrderDetailResponse,
    summary="获取单个订单的详细信息"
)
async def get_order_detail(
    *,
    db: AsyncSession = Depends(get_db),
    order_id: str,
    # 依赖认证：确保只有登录用户才能访问
    # current_user: db_models.User = Depends(get_current_user) 
    # 你可以取消上面这行的注释来启用Token认证
):
    """
    根据提供的订单ID，查询并返回一个预约订单的详细信息。
    """
    # --- 步骤 1: 调用服务函数查询订单 ---
    order = await order_curd.get_order_by_id(db, order_id=order_id)
    
    # --- 步骤 2: 检查订单是否存在 ---
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID为 {order_id} 的订单不存在",
        )
    
    # 可选：检查当前用户是否有权查看此订单
    # if order.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权访问此订单")

    # --- 步骤 3: 构建并返回符合格式的响应 ---
    # 我们使用 Pydantic 模型来构建响应，以确保格式正确
    response = schemas.OrderDetailResponse(
        route=schemas.RouteDetail(
            from_location=order.route.start_location,
            to_location=order.route.end_location
        ),
        bookedTime=order.created_at,
        departureTime=order.schedule.departure_time,
        vehicleNumber=order.bus.bus_number,
        state=map_order_status_to_state(order.status)
    )
    
    return response