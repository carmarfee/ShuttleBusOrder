# app/api/endpoints/get_dynamic_content.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# 请根据你的项目结构调整 import 路径
from app.models.db_models import get_db
from app.models import schemas
from app.services import dynamics_curd

router = APIRouter()

@router.get(
    "/getDynamicContent",
    response_model=schemas.DynamicContentResponse,
    summary="获取单条动态通知的详细内容"
)
async def get_dynamic_content(
    dynamic_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    根据提供的动态ID，获取其完整的标题、内容和附件信息。
    此接口为公开接口，无需认证即可访问。
    """
    # 步骤 1: 调用服务函数查询数据库
    dynamic = await dynamics_curd.get_dynamic_by_id(db, dynamic_id=dynamic_id)

    # 步骤 2: 如果找不到，则返回 404 错误
    if not dynamic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID为 {dynamic_id} 的动态通知不存在"
        )
    
    # 步骤 3: 直接返回 SQLAlchemy 对象
    # FastAPI 会利用 response_model 和 from_attributes=True 配置
    # 自动将其转换为正确的 JSON 响应。
    return dynamic
