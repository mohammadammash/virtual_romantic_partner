from typing import List
# internal:
from ...config.database import UsersCollection
from ...models.user import UserModel
from ...models.message import MessageModel


async def get_all_users() -> List[UserModel]:
    users = await UsersCollection.find().to_list(100)
    return users

async def get_paginated_messages(user_id: str, offset: int) -> List[MessageModel]:
    return []

async def get_count_per_gender():
    return []