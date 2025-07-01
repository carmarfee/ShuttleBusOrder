# 假设此文件路径为 app/services/user_curd.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

# 严格按照你的目录结构进行导入
from app.models import db_models, schemas

# --- 读取操作 (异步) ---

async def get_user(db: AsyncSession, user_id: int) -> Optional[db_models.User]:
    """
    根据用户ID（学工号）异步获取单个用户。
    """
    # 使用 select() 异步查询语法
    query = select(db_models.User).filter(db_models.User.id == user_id)
    result = await db.execute(query)
    # 使用 .scalar_one_or_none() 获取单个对象或None
    return result.scalar_one_or_none()

async def get_user_by_name(db: AsyncSession, name: str) -> Optional[db_models.User]:
    """
    根据用户名异步获取单个用户 (用于唯一性检查)。
    """
    query = select(db_models.User).filter(db_models.User.name == name)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_user_by_phone(db: AsyncSession, phone: str) -> Optional[db_models.User]:
    """
    根据手机号异步获取单个用户 (用于唯一性检查)。
    """
    query = select(db_models.User).filter(db_models.User.phone == phone)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[db_models.User]:
    """
    异步获取用户列表，支持分页。
    """
    query = select(db_models.User).offset(skip).limit(limit)
    result = await db.execute(query)
    # 使用 .scalars().all() 获取对象列表
    return result.scalars().all()


# --- 创建操作 (异步) ---

async def create_user(db: AsyncSession, user: schemas.UserCreate) -> db_models.User:
    """
    异步创建新用户。
    """
    # 将 Pydantic 模型 (user) 的数据解包，创建 SQLAlchemy 模型实例 (db_user)
    db_user = db_models.User(
        id=user.id,
        name=user.name,
        password = user.password,
        phone=user.phone,
        role=user.role,
        department=user.department
    )
    db.add(db_user)
    await db.commit()  # 异步提交
    created_user = await get_user(db, user_id=db_user.id)
    return created_user


# --- 更新操作 (异步) ---

# app/services/user_curd.py

# ... (其他函数和 imports) ...

async def update_user(
    db: AsyncSession, 
    db_user: db_models.User, 
    user_in: schemas.UserUpdate
) -> db_models.User:
    """
    异步更新用户信息。
    """

    update_data = user_in.dict(exclude_unset=True)
    
    # 遍历更新数据，更新 db_user 对象的属性
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user