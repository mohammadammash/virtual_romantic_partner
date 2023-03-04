from fastapi import APIRouter, Body, Depends
# internal:
from . import crud
from ...models.user import LoginUserModel, UserModel, NewUserModel


router = APIRouter(
    prefix="/auth"
)

@router.post("/login", response_description="Login User")
async def post_login_user(data: LoginUserModel = Body(...)):
    return await crud.post_login_user(data=data)

@router.post("/signup", response_description="User Sign Up")
async def signup_user(data: NewUserModel):
    return await crud.post_signup_user(data=data)