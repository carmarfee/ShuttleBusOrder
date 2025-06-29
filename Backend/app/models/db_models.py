from sqlalchemy import Column, String, Integer
from app.database.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    openid = Column(String(128), unique=True, nullable=False)
    nickname = Column(String(50))
    avatar = Column(String(255))