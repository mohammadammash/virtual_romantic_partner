from bson import ObjectId
from fastapi import HTTPException
from passlib.context import CryptContext
from pymongo.collection import ReturnDocument
# internal:
from ...config.database import UsersCollection
from ...models.user import UserModel, UpdateUserModel



async def put_edit_profile(data: UpdateUserModel, user_id: str) -> UserModel:
    user = await UsersCollection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = data.dict(exclude_unset=True) 
    updated_user = await UsersCollection.find_one_and_update(
        {"_id": user["_id"]},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )
    return updated_user