import httpx
from app.core.config import settings

async def get_wx_openid(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.weixin.qq.com/sns/jscode2session",
            params={
                "appid": settings.WX_APPID,
                "secret": settings.WX_SECRET,
                "js_code": code,
                "grant_type": "authorization_code"
            }
        )
        data = resp.json()
        if "errcode" in data:
            raise ValueError(f"WeChat API error: {data}")
        return {
            "openid": data["openid"],
            "session_key": data.get("session_key")
        }