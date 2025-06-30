# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
from contextlib import asynccontextmanager
from app.api.api import api_router
from app.script.importSampleData import insert_sample_data,clear_all_data


# 导入你的数据库配置（假设保存为database.py）
from app.models.db_models import  create_tables


# 应用启动和关闭事件处理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    await create_tables()
    # await insert_sample_data()
    yield
    # 关闭时的清理工作（如果需要）
    # awaitclear_all_data()

# 创建FastAPI应用
app = FastAPI(
    title="智慧班车后端",
    description="基于FastAPI和异步SQLAlchemy的用户管理API",
    version="1.0.0",
    lifespan=lifespan
)

# 分级路由，来自api
app.include_router(api_router,prefix = "/api")

# API路由
@app.get("/", summary="根路径")
async def root():
    return {"message": "用户管理系统API", "status": "运行中"}

