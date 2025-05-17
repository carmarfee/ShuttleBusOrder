from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: AnyUrl = "postgresql+asyncpg://user:pass@localhost:5432/db"
    
    # 微信小程序配置
    WX_APPID: str
    WX_SECRET: str
    WX_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时
    
    # JWT配置
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()