from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field
# internal:
from .message import MessageModel

class UserModel(BaseModel):
    _id: str
    name: str = Field(..., min_length=1)
    email: str = Field(..., regex=r'^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$')
    password: str = Field(..., min_length=6)
    gender: str = Field(..., enum=['male', 'female', 'other'])
    partner_gender: str = Field(..., enum=['male', 'female', 'other'])
    dob: date
    profile_url: Optional[str] = None
    chat: List[MessageModel]

    class Config:
        orm_mode = True
