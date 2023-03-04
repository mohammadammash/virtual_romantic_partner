from fastapi import APIRouter, Depends
from typing import List
# internal:
from . import crud
from ...models.user import NewUserModel, UserModel
from ...models.message import MessageModel, NewMessageModel
from ...dependencies.check_if_user import check_if_user

router = APIRouter(
    prefix="/user",
    dependencies=[Depends(check_if_user)]
)

@router.get("/{offset}", response_description="Get Paginated 10 Messages", response_model=List[MessageModel])
async def get_messages(offset: int, user_id: str = Depends(check_if_user)):
    return await crud.get_paginated_messages(offset=offset, user_id=user_id)

@router.post("/chat", response_description="Send Message", response_model=MessageModel)
async def send_message(new_message: NewMessageModel, user_id: str = Depends(check_if_user)):
    return await crud.post_send_message(data=new_message, user_id=user_id)


