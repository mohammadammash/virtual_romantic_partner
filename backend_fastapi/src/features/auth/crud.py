import base64
from datetime import datetime, timedelta
import imghdr
import os
import uuid
from fastapi import HTTPException
import jwt
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
# internal:
from ...config.database import UsersCollection
from ...config.main import settings
from ...models.user import UserModel, LoginUserModel, NewUserModel


async def post_login_user(data: LoginUserModel):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    user = await UsersCollection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    jwt_payload = {
        "user_id": str(user["_id"]),
        "user_type": user["user_type"],
        "exp": datetime.utcnow() + timedelta(hours=1) # 1hr expiry
    }
    jwt_token = jwt.encode(jwt_payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    return {
        "user": UserModel(**user),
        "token": jwt_token
    }


async def post_signup_user(data: NewUserModel):
    existing_user = await UsersCollection.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
    unhashed_password = data.password
    data.password = pwd_context.hash(data.password)
    
    # Decode the profile_base64 string to bytes and save it as an image file
    user_id = ObjectId()
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

    # Remove the profile_base64 field from the data dictionary
    updated_data = data.dict(exclude={"profile_base64"})
    
    user = jsonable_encoder(updated_data)
    user["profile_url"]=profile_url
    user["_id"]=user_id
    await UsersCollection.insert_one(user)
    
    # Call post_login_user to generate a JWT token and return it with new user data
    login_data = LoginUserModel(email=data.email, password=unhashed_password)
    return await post_login_user(login_data)