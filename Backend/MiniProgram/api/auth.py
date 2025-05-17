from fastapi import APIRouter, Depends, HTTPException
from app.schemas import WechatLoginRequest
from app.services.auth import wechat_login

router = APIRouter()

@router.post("/login/wechat")
async def login_by_wechat(req: WechatLoginRequest):
    try:
        return await wechat_login(req.code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))