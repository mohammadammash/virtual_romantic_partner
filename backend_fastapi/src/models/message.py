from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class MessageModel(BaseModel):
    _id: str
    created_at: datetime = Field(default_factory=datetime.now)
    text: str = Field(..., min_length=1)
    is_author: bool
    image_url: Optional[str] = None
    voice_url: Optional[str] = None
    
    class Config:
        orm_mode = True
