# app/api/endpoints/get_appointmentinfo.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

# 请根据你的项目结构调整 import 路径
from app.core.database import get_db
from app.models import schemas, db_models
from app.services import user_curd # 或者你创建的 order_curd

router = APIRouter()

def derive_credit_status(order_status: db_models.OrderStatus) -> str:
    """
    根据订单状态衍生出信用情况的辅助函数。
    你可以根据实际业务规则扩展此逻辑。
    """
    if order_status == db_models.OrderStatus.COMPLETED:
        return "信用良好"
    elif order_status == db_models.OrderStatus.CANCELLED:
        return "有待观察 (已取消)"
    elif order_status == db_models.OrderStatus.PENDING:
        return "正常 (待处理)"
    elif order_status == db_models.OrderStatus.CONFIRMED:
        return "正常 (已确认)"
    return "未知"


@router.get(
    "/getAppointmentInfo", 
    response_model=schemas.AppointmentInfoResponse,
    summary="获取单个预约订单的详细信息"
)
async def get_appointment_info(
    *,
    db: AsyncSession = Depends(get_db),
    # 将 order_no 作为查询参数
    order_no: str = Query(..., description="要查询的订单编号")
):
    """
    根据提供的订单编号，查询并返回一个预约订单的详细信息，
    包括订单状态和衍生的信用情况。
    """
    # --- 步骤 1: 调用服务函数查询订单 ---
    # 假设你已将 get_order_by_order_no 添加到 user_curd 中
    order = await user_curd.get_order_by_order_no(db, order_no=order_no)
    
    # --- 步骤 2: 检查订单是否存在 ---
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"订单号为 {order_no} 的订单不存在",
        )

    # --- 步骤 3: 衍生信用情况 ---
    credit_status = derive_credit_status(order.status)
    
    # --- 步骤 4: 构建并返回响应数据 ---
    # 我们手动构建字典，以确保所有字段都正确填充
    response_data = {
        "id": order.id,
        "order_no": order.order_no,
        "status": order.status,
        "user_id": order.user.id,
        "user_name": order.user.name,
        "route_id": order.route_id,
        "bus_id": order.bus_id,
        "schedule_id": order.schedule_id,
        "credit_status": credit_status
    }
    
    return response_data