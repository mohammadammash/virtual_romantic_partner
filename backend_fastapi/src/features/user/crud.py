from typing import List
from fastapi.encoders import jsonable_encoder
# internal:
from ...config.database import UsersCollection
from ...models.user import UserModel, NewUserModel
from ...models.message import MessageModel, NewMessageModel

async def post_signup_user(data: NewUserModel) -> UserModel:
    user = jsonable_encoder(data)
    new_user = await UsersCollection.insert_one(user)
    created_user = await UsersCollection.find_one({"_id": new_user.inserted_id})
    return created_user


async def get_paginated_messages(user_id: str, offset: int) -> List[MessageModel]:
    return []


async def post_send_message(data: NewMessageModel) -> MessageModel:
    message = jsonable_encoder(data)
    new_message = await UsersCollection.insert_one(message)
    sent_message = await UsersCollection.find_one({"_id": new_message.inserted_id})
    return sent_message