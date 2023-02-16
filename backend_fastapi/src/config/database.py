import os
from motor import motor_asyncio
# internal
from .main import settings

print(settings.MONGODB_URI)
client = motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)

db = client.virtualpartner_db
UsersCollection = db.users
