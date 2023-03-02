from bson import ObjectId
# internal:
from ...config.database import UsersCollection
from ...models.user import UserModel

async def post_login_user(user_id: str) -> UserModel:
    user = await UsersCollection.find_one({"_id": ObjectId(user_id)})
    return user

async def put_edit_profile() -> UserModel:
    user = await UsersCollection.find_one({"_id": ObjectId("64005e70cf5c276361cf0ee1")})
    return user