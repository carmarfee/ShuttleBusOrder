# app/core/wechat_utils.py

import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

from app.core.config import settings

# 简单的内存缓存，用于存储 access_token
class AccessTokenCache:
    def __init__(self):
        self._token: str | None = None
        self._expiry_time: datetime | None = None

    def get_token(self) -> str | None:
        """如果 token 有效则返回，否则返回 None"""
        if self._token and self._expiry_time and datetime.now() < self._expiry_time:
            return self._token
        return None

    def set_token(self, token: str, expires_in: int):
        """设置 token 并计算过期时间"""
        self._token = token
        # 设置5分钟的安全缓冲期，防止 token 在临界点失效
        self._expiry_time = datetime.now() + timedelta(seconds=expires_in - 300)

token_cache = AccessTokenCache()
# 创建一个锁，防止在 token 失效时多个请求同时去获取新 token
token_lock = asyncio.Lock()

async def get_access_token() -> Dict[str, Any]:
    """
    异步获取微信小程序 access_token，并使用缓存。
    """
    # 首先检查缓存
    cached_token = token_cache.get_token()
    if cached_token:
        return {'success': True, 'access_token': cached_token}

    # 如果缓存失效，加锁以获取新 token
    async with token_lock:
        # 再次检查缓存，因为在等待锁的时候可能其他协程已经获取了新 token
        cached_token = token_cache.get_token()
        if cached_token:
            return {'success': True, 'access_token': cached_token}

        # 缓存中没有，发起 HTTP 请求
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            'grant_type': 'client_credential',
            'appid': settings.WX_APPID,
            'secret': settings.WX_SECRET
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10)
                response.raise_for_status() # 如果 http 状态码不是 2xx，则抛出异常
                result = response.json()

            if 'errcode' in result and result['errcode'] != 0:
                return {'success': False, **result}
            
            # 成功获取，更新缓存
            token_cache.set_token(result['access_token'], result['expires_in'])
            return {'success': True, **result}

        except httpx.HTTPStatusError as e:
            return {'success': False, 'errcode': -1, 'errmsg': f"HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {'success': False, 'errcode': -1, 'errmsg': str(e)}

async def send_subscribe_message(access_token: str, openid: str, template_id: str, data: dict, page: str = None) -> Dict[str, Any]:
    """
    异步发送微信小程序订阅消息。
    """
    url = f"https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={access_token}"
    payload = {"touser": openid, "template_id": template_id, "data": data}
    if page:
        payload["page"] = page
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
        
        return {'success': result.get('errcode', -1) == 0, **result}
        
    except Exception as e:
        return {'success': False, 'errcode': -1, 'errmsg': str(e)}

