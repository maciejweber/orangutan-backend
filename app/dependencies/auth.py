from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt import decode_jwt_token
from app.users.repositories import get_user_details_from_db_by_email
from app.users.models import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = credentials.credentials
    payload = decode_jwt_token(token)
    user_email = payload.get("sub")
    if user_email is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = await get_user_details_from_db_by_email(user_email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return User(**user)
