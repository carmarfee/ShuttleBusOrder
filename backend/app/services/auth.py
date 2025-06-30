from app.utils.wx import get_wx_openid
from app.core.security import create_access_token

async def wechat_login(code: str):
    wx_data = await get_wx_openid(code)
    
    # 这里可以添加用户入库逻辑
    user = await UserService.get_or_create(wx_data["openid"])
    
    return {
        "access_token": create_access_token({"sub": user.id}),
        "user_info": user.dict()
    }