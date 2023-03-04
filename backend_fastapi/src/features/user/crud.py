from typing import List
from fastapi import HTTPException
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
# internal:
from ...config.database import UsersCollection
from ...models.message import MessageModel, NewMessageModel
from ..helpers.get_paginated_messages import get_paginated_messages_helper


async def get_paginated_messages( offset: int, user_id: str) -> List[MessageModel]:
    return await get_paginated_messages_helper(user_id=user_id,offset=offset)


async def post_send_message(data: NewMessageModel, user_id: str)->MessageModel:
    user = await UsersCollection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    message = jsonable_encoder(data)
    message_id = ObjectId()
    message.update({"_id": str(message_id)})
    # prepare response message
    response_message = MessageModel(
        id=str(ObjectId()),
        is_author=False,
        text="hey_dude",
    )
    
    # push both message once to the db
    result = await UsersCollection.update_one({"_id": user["_id"]}, {"$push": {"chats": {"$each": [message, jsonable_encoder(response_message)]}}})
    
    if not result.modified_count:
        raise HTTPException(status_code=500, detail="Failed to send message")
    
    return response_message