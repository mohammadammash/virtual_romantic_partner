from typing import List
from bson import ObjectId
from fastapi import HTTPException
# internal:
from ...config.database import UsersCollection
from ...models.user import UserModel
from ...models.message import MessageModel
from ..helpers.get_paginated_messages import get_paginated_messages_helper

async def get_all_users() -> List[UserModel]:
    users = await UsersCollection.find().to_list(100)
    return users

async def get_paginated_messages(user_id: str, offset: int) -> List[MessageModel]:
    return await get_paginated_messages_helper(user_id=user_id, offset=offset)

async def get_count_per_gender():
    return []