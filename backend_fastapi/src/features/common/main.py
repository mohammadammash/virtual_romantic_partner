from fastapi import APIRouter, Body, Depends
# internal:
from . import crud
from ...models.user import UserModel, UpdateUserModel
from ...dependencies.auth import verify_authentication


router = APIRouter(
    prefix="/common",
    dependencies=[Depends(verify_authentication)]
)

@router.put("/profile", response_description="Edit Profile", response_model=UserModel)
async def put_edit_profile(data: UpdateUserModel, payload=(Depends(verify_authentication))):
    return await crud.put_edit_profile(data=data, user_id=payload["user_id"])
