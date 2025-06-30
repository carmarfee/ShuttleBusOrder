# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
from contextlib import asynccontextmanager

# 导入你的数据库配置（假设保存为database.py）
from app.models.db_models import get_db, create_tables, User

# Pydantic模型用于请求和响应
class UserCreate(BaseModel):
    id: int = Field(..., description="用户ID，学工号")
    name: str = Field(..., min_length=1, max_length=50, description="用户名称")
    phone: str = Field(..., min_length=1, max_length=20, description="手机号码")
    role: str = Field(..., min_length=1, max_length=20, description="用户角色")
    department: Optional[str] = Field(None, max_length=50, description="部门")

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    role: Optional[str] = Field(None, min_length=1, max_length=20)
    department: Optional[str] = Field(None, max_length=50)

class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    role: str
    department: Optional[str]
    
    class Config:
        from_attributes = True

# 应用启动和关闭事件处理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    await create_tables()
    yield
    # 关闭时的清理工作（如果需要）

# 创建FastAPI应用
app = FastAPI(
    title="智慧班车后端",
    description="基于FastAPI和异步SQLAlchemy的用户管理API",
    version="1.0.0",
    lifespan=lifespan
)

# API路由
@app.get("/", summary="根路径")
async def root():
    return {"message": "用户管理系统API", "status": "运行中"}

