from fastapi import HTTPException, Depends
# internal
from .auth import verify_authentication

async def check_if_user(payload = Depends(verify_authentication)):
    user_type = payload.get("user_type")
    if user_type != "user":
        raise HTTPException(status_code=401, detail="User not authorized to perform this action")
    return payload.get("user_id")