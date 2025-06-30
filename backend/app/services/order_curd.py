from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models import db_models
async def get_order_by_order_no(db: AsyncSession, order_no: str) -> Optional[db_models.Order]:
    """
    根据订单号异步获取单个订单，并预加载关联的用户信息。
    """
    query = (
        select(db_models.Order)
        .options(joinedload(db_models.Order.user)) # 使用 joinedload 预加载用户信息
        .filter(db_models.Order.order_no == order_no)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()