# core/config.py

import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# 加载 .env 文件中的环境变量
load_dotenv()

class Settings(BaseSettings):
    """
    应用配置类，使用 Pydantic 进行类型校验。
    """
    # 数据库连接URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # 微信小程序配置
    WX_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时

    # --- 新增微信小程序配置 ---
    WX_APPID: str
    WX_SECRET: str
    
    # --- 新增微信订阅消息模板ID ---
    WX_ORDER_TEMPLATE_ID: str = "d0CikXwRfK5apE3Yqo1wsiicNwW0mIodgyfXlZzF55M" # 这是一个示例，请替换成你自己的

    # JWT 令牌配置
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    class Config:
        case_sensitive = True

# 创建配置实例，方便在其他地方导入使用
settings = Settings()
