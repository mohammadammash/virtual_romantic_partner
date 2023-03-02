from fastapi import APIRouter, Depends, Request
from typing import List
# internal:
from . import crud
from ...models.user import NewUserModel, UserModel
from ...models.message import MessageModel, NewMessageModel

router = APIRouter(
    # dependencies=[Depends(verify_authentication)]
)

@router.get("/{user_id}/{offset}", response_description="Get Paginated 10 Messages", response_model=List[MessageModel])
async def get_messages(user_id: str, offset: int):
    return await crud.get_paginated_messages(user_id=user_id,offset=offset)

@router.post("/chat", response_description="Send Message", response_model=MessageModel)
async def send_message(new_message: NewMessageModel):
    return await crud.post_send_message(data=new_message)

@router.post("/signup", response_description="User Sign Up", response_model=UserModel)
async def signup_user(data: NewUserModel):
    return await crud.post_signup_user(data=data)


