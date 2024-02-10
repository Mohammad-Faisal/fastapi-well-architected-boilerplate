from fastapi import APIRouter, Depends
from typing import Mapping

from src.api.user.service import UserService
from src.api.user.schemas import UserCreateInput, UserUpdateInput
from src.api.user.dependencies import get_user

router = APIRouter()


@router.get("/")
async def read_users(user_service: UserService = Depends()):
    users = user_service.get()
    return users


@router.post("/")
async def create_user(
    user_create_input: UserCreateInput, user_service: UserService = Depends()
):
    user = user_service.create(user_create_input)
    return user


@router.get("/{user_id}")
async def read_user(
    user_id: int,
    user_service: UserService = Depends(),
    user: Mapping = Depends(get_user),
):
    user = user_service.get_by_id(user_id)
    return user


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update_input: UserUpdateInput,
    user_service: UserService = Depends(),
    user: Mapping = Depends(get_user),
):
    user = user_service.update(user_id, user_update_input)
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(),
    user: Mapping = Depends(get_user),
):
    user = user_service.delete(user_id)
    return user
