from fastapi import APIRouter, HTTPException
from app.users.services import get_users, get_user_details, login_user
from app.users.models import LoginUser

router = APIRouter()


@router.get("/")
async def get_users_endpoint():
    users = await get_users()
    return users


@router.get("/{id}")
async def get_users_endpoint(id: int):
    users = await get_user_details(id)
    return users


@router.post("/login")
async def login_endpoint(login_request: LoginUser):
    if login_request.password != login_request.confirm_password:
        raise HTTPException(
            status_code=400, detail="Password and confirm password do not match"
        )

    users = await login_user(login_request.email, login_request.password)
    return users
