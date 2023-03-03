from typing import List
from fastapi import HTTPException
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
# internal:
from ...config.database import UsersCollection
from ...models.user import UserModel, NewUserModel
from ...models.message import MessageModel, NewMessageModel


async def post_signup_user(data: NewUserModel) -> UserModel:
    existing_user = await UsersCollection.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
    data.password = pwd_context.hash(data.password)
    
    user = jsonable_encoder(data)
    new_user = await UsersCollection.insert_one(user)
    created_user = await UsersCollection.find_one({"_id": new_user.inserted_id})
    return created_user


async def get_paginated_messages(user_id: str, offset: int) -> List[MessageModel]:
    user = await UsersCollection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    messages = user.get("chats", [])
    start = offset
    end = start + 10
    paginated_messages = [MessageModel(**message) for message in messages[start:end]]
    return paginated_messages


async def post_send_message(data: NewMessageModel)->MessageModel:
    user = await UsersCollection.find_one({"_id": ObjectId("64005e70cf5c276361cf0ee1")})
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