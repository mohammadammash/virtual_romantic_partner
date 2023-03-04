import base64
import imghdr
import os
import uuid
from fastapi import HTTPException
from ...config.main import settings


async def save_profile_image(data, user_id):
    if not data.profile_base64:
        return None
    
    profile_bytes = base64.b64decode(data.profile_base64)
    extension = imghdr.what(None, h=profile_bytes)
    if not extension:
        raise HTTPException(status_code=400, detail="Invalid profile image")
    
    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(settings.PROFILE_IMAGE_DIR, str(user_id))
    os.makedirs(filepath, exist_ok=True)
    
    with open(os.path.join(filepath, filename), "wb") as f:
        f.write(profile_bytes)
    
    return f"{filepath}\{filename}"