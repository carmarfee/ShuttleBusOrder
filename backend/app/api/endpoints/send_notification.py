# app/api/endpoints/send_notification.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.db_models import get_db
from app.models import db_models
from app.services import user_curd
from app.utils import wx # 导入我们新的微信工具
from app.core.config import settings

router = APIRouter()

@router.post("/sendTestNotification", summary="发送一条测试订阅消息")
async def send_test_notification(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: str # 将 user_id 作为请求体的一部分或查询参数
):
    """
    向指定用户发送一条测试性的订单状态通知。
    """
    # 1. 获取用户信息，主要是为了 openid
    user = await user_curd.get_user(db, user_id=user_id)
    if not user or not user.openid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户 {user_id} 不存在或未绑定微信OpenID"
        )

    # 2. 获取 access_token
    token_result = await wx.get_access_token()
    if not token_result.get('success'):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取微信access_token失败: {token_result.get('errmsg')}"
        )
    access_token = token_result['access_token']

    # 3. 准备消息模板数据
    # 这部分数据可以根据你的业务场景动态生成
    message_data = {
        "character_string1": {"value": "TEST00000001"},
        "phrase5": {"value": "测试通过"},
        "thing3": {"value": user.name},
        "thing6": {"value": "这是一条来自后端的测试通知，收到请忽略。"}
    }

    # 4. 发送订阅消息
    send_result = await wx.send_subscribe_message(
        access_token=access_token,
        openid=user.openid,
        template_id=settings.WX_ORDER_TEMPLATE_ID,
        data=message_data,
        page="pages/index/index" # 点击消息后跳转的页面
    )

    # 5. 根据发送结果返回响应
    if not send_result.get('success'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"发送订阅消息失败: {send_result.get('errmsg')}"
        )

    return {"message": "测试通知发送成功", "details": send_result}
