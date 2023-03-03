from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
# internal
from ..config.mongodb_objectid import PyObjectId

class MessageModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    text: str = Field(..., min_length=1)
    is_author: bool
    image_url: Optional[str] = None
    voice_url: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "created_at": "2023-02-22",
                "text": "Hello Babe",
                "is_author": True,
                "image_url": "db/public/images/user1.png",
                "voice_url": "db/public/voices/user1.mp3"
            }
        }
        
class NewMessageModel(BaseModel):
    text: str = Field(..., min_length=1)
    is_author: Optional[bool] = True
    image_base64: Optional[str] = None
    voice_data: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "text": "Hello Honey!!",
                "is_author": False,
                "image_base64": "FGIDSGIKSDIF23W",
                "voice_data": "THISISMYVOICEDATA"
            }
        }
