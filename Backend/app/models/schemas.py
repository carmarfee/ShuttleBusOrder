from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
class WxUserInfo(BaseModel):
    """微信解密后的用户数据"""
    openId: str
    nickName: str
    gender: int
    city: str
    province: str
    country: str
    avatarUrl: str
    unionId: Optional[str]
    watermark: dict  # 包含appid和时间戳