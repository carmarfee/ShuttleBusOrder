import json
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Union, Dict, List
from functools import singledispatch

class JSONEncoder(json.JSONEncoder):
    """
    增强的JSON编码器，支持更多数据类型：
    - datetime/date 转为 ISO8601 字符串
    - Decimal 转为 float
    - bytes 转为 base64 字符串
    - 支持自定义类型的 __json__ 方法
    """
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')
        elif hasattr(obj, '__json__'):
            return obj.__json__()
        return super().default(obj)

@singledispatch
def json_serialize(obj: Any) -> Any:
    """通用JSON序列化入口"""
    return obj

@json_serialize.register(datetime)
@json_serialize.register(date)
def _(obj: Union[datetime, date]) -> str:
    return obj.isoformat()

@json_serialize.register(Decimal)
def _(obj: Decimal) -> float:
    return float(obj)

@json_serialize.register(bytes)
def _(obj: bytes) -> str:
    return obj.decode('utf-8', errors='replace')

def safe_json_loads(json_str: str) -> Union[Dict, List, None]:
    """
    安全的JSON解析（带异常捕获）
    
    Args:
        json_str: 需要解析的JSON字符串
        
    Returns:
        解析后的字典/列表，解析失败时返回None
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return None

def json_dumps(obj: Any, **kwargs) -> str:
    """
    增强的JSON序列化
    
    Args:
        indent: 缩进空格数（微信小程序建议2）
        ensure_ascii: 是否转义非ASCII字符（微信建议False）
    """
    kwargs.setdefault('ensure_ascii', False)
    kwargs.setdefault('indent', 2)
    return json.dumps(obj, cls=JSONEncoder, **kwargs)

def format_wechat_data(data: Dict) -> Dict:
    """
    格式化微信接口返回的数据：
    - 将snake_case转为camelCase
    - 处理空值字段
    """
    formatted = {}
    for k, v in data.items():
        if v is None:
            continue
        # snake_case to camelCase
        if '_' in k:
            parts = k.split('_')
            new_key = parts[0] + ''.join(p.capitalize() for p in parts[1:])
        else:
            new_key = k
        formatted[new_key] = json_serialize(v)
    return formatted

def parse_wechat_response(response_text: str) -> Dict:
    """
    解析微信接口响应（自动处理错误码）
    
    Example:
        {
            "errcode": 0,
            "errmsg": "ok",
            "openid": "OPENID",
            "session_key": "SESSION_KEY"
        }
    """
    data = safe_json_loads(response_text)
    if not data:
        raise ValueError("Invalid WeChat response format")
    
    if 'errcode' in data and data['errcode'] != 0:
        raise ValueError(
            f"WeChat API error {data['errcode']}: {data.get('errmsg', 'Unknown error')}"
        )
    return data

def deep_merge(a: Dict, b: Dict) -> Dict:
    """
    深度合并两个字典（用于合并微信配置）
    """
    result = a.copy()
    for k, v in b.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result