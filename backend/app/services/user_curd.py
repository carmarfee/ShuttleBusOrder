# 假设此文件路径为 app/services/user_curd.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.core.security import get_password_hash
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

async def create_user(db: AsyncSession, user: schemas.UserCreateByAdmin) -> db_models.User:
    """
    异步创建新用户，并使用提供的密码进行哈希。
    """
    # 1. 为提供的密码生成哈希值
    hashed_password = get_password_hash(user.password)
    
    # 2. 创建数据库模型实例
    db_user = db_models.User(
        id=user.id,
        name=user.name,
        password=hashed_password, # 存入哈希后的密码
        phone=user.phone,
        role=user.role,
        department=user.department
    )
    db.add(db_user)
    await db.commit()
    
    # 使用 get_user 重新获取，避免 refresh 的问题
    created_user = await get_user(db, user_id=db_user.id)
    return created_user

# --- delete_user 函数 ---
async def delete_user(db: AsyncSession, user_id: str) -> bool:
    """
    根据用户ID删除一个用户。
    如果用户存在并被删除，返回 True，否则返回 False。
    """
    user_to_delete = await get_user(db, user_id=user_id)
    if not user_to_delete:
        return False
    
    await db.delete(user_to_delete)
    await db.commit()
    return True



# --- 更新操作 (异步) ---



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



async def update_user_openid(db: AsyncSession, *, db_user: db_models.User, openid: str) -> db_models.User:
    """
    为指定的用户对象更新或存储其 OpenID。
    """
    # 将新的 openid 赋值给用户对象的 openid 字段
    db_user.openid = openid
    
    # 将更改添加到会话中
    db.add(db_user)
    
    # 提交事务以保存更改
    await db.commit()
    
    # 刷新对象以获取数据库中的最新状态
    await db.refresh(db_user)
    
    return db_user

async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[db_models.User]:
    """异步获取用户列表，支持分页。"""
    query = select(db_models.User).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()