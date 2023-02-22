from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId
# internal:
from .message import MessageModel
from ..config.mongodb_objectid import PyObjectId


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: str = Field(..., regex=r'^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$')
    password: str = Field(..., min_length=6)
    gender: str = Field(..., enum=['male', 'female', 'other'])
    partner_gender: str = Field(..., enum=['male', 'female', 'other'])
    dob: date
    profile_url: Optional[str] = None
    chat: Optional[List[MessageModel]] = []
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "gender": "male",
                "partner_gender": "female",
                "dob": "2023-02-22",
                "profile_url": "/public/images/ahmad@gmail.com24532432",
                "chat": "[]",
            }
        }

class NewUserModel(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., regex=r'^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$')
    password: str = Field(..., min_length=6)
    gender: str = Field(..., enum=['male', 'female', 'other'])
    partner_gender: str = Field(..., enum=['male', 'female', 'other'])
    dob: date
    profile_base64: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "123PleaseDontUseMe",
                "gender": "female",
                "partner_gender": "male",
                "dob": "2023-02-18",
                "profile_base64": "GSFDKGSID#$#@#LFDSFD",
            }
        }


