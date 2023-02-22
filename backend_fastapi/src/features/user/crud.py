from typing import List
from fastapi.encoders import jsonable_encoder
# internal:
from ...config.database import UsersCollection
from ...models.user import UserModel, NewUserModel
from ...models.message import MessageModel

async def get_all_users() -> List[UserModel]:
    users = await UsersCollection.find().to_list(1000)
    return users


async def post_signup_user(data: NewUserModel) -> UserModel:
    user = jsonable_encoder(data)
    new_user = await UsersCollection.insert_one(user)
    created_user = await UsersCollection.find_one({"_id": new_user.inserted_id})
    return created_user


async def get_paginated_messages(offset: int) -> List[MessageModel]:
    return []
