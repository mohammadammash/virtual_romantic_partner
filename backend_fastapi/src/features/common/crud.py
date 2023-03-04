import base64
import imghdr
import os
import uuid
from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.collection import ReturnDocument
# internal:
from ...config.database import UsersCollection
from ...config.main import settings
from ...models.user import UserModel, UpdateUserModel



async def put_edit_profile(data: UpdateUserModel, user_id: str) -> UserModel:
    user = await UsersCollection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if data.profile_base64:
        profile_bytes = base64.b64decode(data.profile_base64)
        extension = imghdr.what(None, h=profile_bytes)
        if extension:
            filename = f"{uuid.uuid4()}.{extension}"
            filepath =os.path.join(settings.PROFILE_IMAGE_DIR, str(user_id))
            os.makedirs(filepath, exist_ok=True)
            
            with open(os.path.join(filepath, filename), "wb") as f:
                f.write(profile_bytes)
            # Set the profile_url field to the URL of the saved image file
            profile_url = f"{filepath}\{filename}"
            
        else:
            # If the profile_base64 string is not a valid image, raise an exception
            raise HTTPException(status_code=400, detail="Invalid profile image")

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