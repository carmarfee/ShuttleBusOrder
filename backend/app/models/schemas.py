# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

# Pydantic模型用于请求和响应


# ===============================================================
# 令牌相关的模型 
# ===============================================================

class Token(BaseModel):
    """
    定义JWT令牌的响应格式。
    """
    access_token: str
    token_type: str




# ===============================================================
# 用户相关的模型 
# ===============================================================


class UserCreate(BaseModel):
    id: str = Field(..., description="用户ID，学工号")
    password: str = Field(..., min_length=1, max_length=50, description="用户密码")
    name: str = Field(..., min_length=1, max_length=50, description="用户名称")
    phone: str = Field(..., min_length=1, max_length=20, description="手机号码")
    role: str = Field(..., min_length=1, max_length=20, description="用户角色")
    department: Optional[str] = Field(None, max_length=50, description="部门")

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=50, description="用户密码")
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    role: Optional[str] = Field(None, min_length=1, max_length=20)
    department: Optional[str] = Field(None, max_length=50)

class UserResponse(BaseModel):
    id: str
    name: str
    phone: str
    role: str
    department: Optional[str]
    
    class Config:
        from_attributes = True


# ===============================================================
# auth/login
# ===============================================================

class LoginRequest(BaseModel):
    """
    定义登录接口的请求体格式 (简化版)。
    """
    passwordistr = Field(..., description="用deng'lu'mi'ma学工号")
    password: str = Field(..., description="用户密码")
    role: str = Field(..., description="用户角色")


class LoginResponse(BaseModel):
    """
    定义登录成功后的响应格式 (保持不变)。
    """
    token: str
    userinfo: "UserResponse"


# 更新 LoginResponse 的模型引用
LoginResponse.update_forward_refs(UserResponse=UserResponse)