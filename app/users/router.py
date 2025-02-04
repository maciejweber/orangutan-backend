from fastapi import APIRouter, HTTPException, Depends
from app.users.services import get_users, get_user_details, login_user, register_user
from app.users.models import LoginUser, RegisterUser, User
from app.dependencies.auth import get_current_user


router = APIRouter()


# @router.get("/{id}")
# async def get_users_endpoint(id: int):
#     users = await get_user_details(id)
#     return users


@router.post("/login")
async def login_endpoint(login_request: LoginUser):
    users = await login_user(login_request.email, login_request.password)
    return users


@router.post("/register")
async def register_endpoint(register_request: RegisterUser):
    print("register")
    if register_request.password != register_request.confirm_password:
        raise HTTPException(
            status_code=400, detail="Password and confirm password do not match"
        )

    user = await register_user(register_request.email, register_request.password)
    return user
