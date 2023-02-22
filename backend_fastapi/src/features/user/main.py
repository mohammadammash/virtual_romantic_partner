from fastapi import APIRouter, Depends, Request
from typing import List
# internal:
from . import crud
from ...models.user import NewUserModel, UserModel

router = APIRouter(
    prefix="/user",
    # dependencies=[Depends(verify_authentication)]
)

@router.get("/", response_description="All Users", response_model=List[UserModel])
async def get_all_users():
    return await crud.get_all_users()

@router.post("/", response_description="User Sign Up", response_model=UserModel)
async def signup_user(data: NewUserModel):
    return await crud.post_signup_user(data=data)


