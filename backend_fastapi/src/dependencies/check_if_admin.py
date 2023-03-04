from fastapi import HTTPException, Depends
# internal
from .auth import verify_authentication

async def check_if_admin(payload = Depends(verify_authentication)):
    user_type = payload.get("user_type")
    if user_type != "admin":
        raise HTTPException(status_code=401, detail="User not authorized to perform this action")