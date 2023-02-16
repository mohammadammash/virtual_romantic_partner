from typing import List
# internal:
from ...config.database import UsersCollection
from ...models import UserModel

async def get_all_users() -> List[UserModel]:
    users = await UsersCollection.find().to_list(1000)
    return users
