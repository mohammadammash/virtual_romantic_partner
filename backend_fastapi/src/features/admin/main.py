from fastapi import APIRouter, Depends
from typing import List
# internal:
from . import crud
from ...models.user import UserModel
from ...models.message import MessageModel
from ...dependencies.check_if_admin import check_if_admin

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(check_if_admin)]
)

@router.get("/users", response_description="All Users", response_model=List[UserModel])
async def get_all_users():
    return await crud.get_all_users()

@router.get("/users/gender", response_description="Get Users Count Per Gender")
async def get_count_of_genders():
    return await crud.get_count_per_gender()

@router.get("/{user_id}/{offset}", response_description="Get Paginated 10 Messages", response_model=List[MessageModel])
async def get_messages(user_id: str, offset: int):
    return await crud.get_paginated_messages(user_id=user_id,offset=offset)

