from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import os
from pydantic import BaseModel
import logging






logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为 DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # 输出到控制台
)

# 启用 databases 库的调试日志
logging.getLogger("databases").setLevel(logging.DEBUG)


class User(BaseModel):
    """
    测试数据结构
    """

    name: str
    id: int
    email: str



# FastAPI 应用
app = FastAPI(
    
)  # 这里注册lifespan函数，不注册就没用了，函数根本不会调用


# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    logging.debug("This is a debug message")
    return {"message": "Hello World,This is main Page"}


@app.get("/qqwyx")
async def root():
    return {"message": "Hello World"}


@app.post("/sqli/sqli_nu")
async def sqli_num_1(user: User):

    return user




if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")