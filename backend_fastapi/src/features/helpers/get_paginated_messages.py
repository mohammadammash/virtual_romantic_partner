from typing import List
from bson import ObjectId
from fastapi import HTTPException
#internal:
from ...models.message import MessageModel
from ...config.database import UsersCollection


async def get_paginated_messages_helper(user_id: str, offset: int)-> List[MessageModel]:
    user = await UsersCollection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    messages = user.get("chats", [])
    start = offset
    end = start + 10
    paginated_messages = [MessageModel(**message) for message in messages[start:end]]
    return paginated_messages
