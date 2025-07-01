# app/api/endpoints/manage_users.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import get_db
from app.models import schemas, db_models
from app.services import user_curd
from app.core.auth import get_current_admin_user # 导入管理员认证守卫

router = APIRouter()

@router.post(
    "/addUser",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK,
    summary="管理员添加新用户"
)
async def add_new_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: schemas.UserCreateByAdmin,
    admin_user: db_models.User = Depends(get_current_admin_user)
):
    """
    由管理员创建一个新的用户账户。
    - 需要管理员权限。
    - 密码将被哈希后存储。
    """
    # 检查用户ID或手机号是否已存在
    existing_user_by_id = await user_curd.get_user(db, user_id=user_in.id)
    if existing_user_by_id:
        raise HTTPException(status.HTTP_409_CONFLICT, f"用户ID '{user_in.id}' 已被注册。")
    
    # 你可能还需要一个 get_user_by_phone 的服务函数来检查手机号
    # existing_user_by_phone = await user_curd.get_user_by_phone(db, phone=user_in.phone)
    # if existing_user_by_phone:
    #     raise HTTPException(status.HTTP_409_CONFLICT, f"手机号 '{user_in.phone}' 已被注册。")

    new_user = await user_curd.create_user(db, user=user_in)
    return new_user


@router.delete(
    "/deleteUser",
    status_code=status.HTTP_200_OK,
    summary="管理员删除用户"
)
async def remove_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: str,
    admin_user: db_models.User = Depends(get_current_admin_user)
):
    """
    由管理员根据用户ID删除一个用户账户。
    - 需要管理员权限。
    - 如果用户不存在，操作也会静默成功。
    """
    # 防止管理员误删自己
    if user_id == admin_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "不能删除自己的账户。")

    deleted = await user_curd.delete_user(db, user_id=user_id)
    if not deleted:
        
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"用户ID为 '{user_id}' 的用户不存在。")
        # pass # 保持静默成功
    
    return Response(status_code=status.HTTP_200_OK)

@router.put(
    "/updateUser",
    status_code=status.HTTP_200_OK,
    summary="更新用户信息"
)
async def update_user_info(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: str,
    name: str,
    password: str,
    role: str,
    phone: str,
    department: str
    # admin_user: db_models.User = Depends(get_current_admin_user)
):
    """
    由管理员根据用户ID更新一个用户账户的信息。
    - 需要权限。
    - 不会更新密码。
    """

    user_in = schemas.UserUpdate(
        name = name,
        password = password,
        role = role,
        phone = phone,
        department = department
    )

    user_to_update = await user_curd.get_user(db, user_id=user_id)
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户ID为 '{user_id}' 的用户不存在。"
        )

    await user_curd.update_user(db, db_user=user_to_update, user_in=user_in)
    return 
