from asyncpg import Pool
from app.users.queries import GET_USERS
from app.users.models import UserBasic, UserLogin
from app.users.queries import GET_USERS_EMAIL_AND_PASSWORD


async def get_users(db_pool: Pool):
    try:
        async with db_pool.acquire() as connection:
            rows = await connection.fetch(GET_USERS)
            return [UserBasic(**dict(row)) for row in rows]
    except Exception as e:
        print(f"Error fetching users: {e}")
        raise


async def authenticate_user(db_pool: Pool, email: str, passwd: str):
    try:
        async with db_pool.acquire() as connection:
            row = await connection.fetchrow(GET_USERS_EMAIL_AND_PASSWORD, email, passwd)
            if row:
                return {"id": row["id"], "email": row["email"]}
            else:
                return None
    except Exception as e:
        print(f"Error fetching users: {e}")
        raise
