from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.collection import ReturnDocument
# internal:
from ...config.database import UsersCollection
from ...models.user import UserModel, UpdateUserModel
from ..helpers.base64_image_upload import save_profile_image


async def put_edit_profile(data: UpdateUserModel, user_id: str) -> UserModel:
    user = await UsersCollection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile_url = await save_profile_image(data, user_id)

    updated_data = data.dict(exclude_unset=True) 
    updated_data = data.dict(exclude={"profile_base64"})
    
    user = jsonable_encoder(updated_data)
    if profile_url:
        user["profile_url"]=profile_url
        
    updated_user = await UsersCollection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": user},
        return_document=ReturnDocument.AFTER
    )
    return updated_user