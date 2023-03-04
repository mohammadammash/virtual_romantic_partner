from bson import ObjectId
from fastapi import HTTPException
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
# internal:
from ...config.database import UsersCollection
from ...models.user import UserModel, LoginUserModel, NewUserModel


async def post_login_user(data: LoginUserModel) -> UserModel:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    user = await UsersCollection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    return UserModel(**user)


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