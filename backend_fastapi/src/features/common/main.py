from fastapi import APIRouter, Body
# internal:
from . import crud
from ...models.user import UserModel

router = APIRouter(
    # dependencies=[Depends(verify_authentication)]
)

@router.post("/login", response_description="Login User", response_model=UserModel)
async def post_login_user(user_id: str = Body(...)):
    return await crud.post_login_user(user_id=user_id)

@router.put("/profile", response_description="Edit Profile", response_model=UserModel)
async def put_edit_profile():
    return await crud.put_edit_profile()
