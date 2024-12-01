from asyncpg import Pool
from app.users.queries import GET_USERS
from app.users.models import UserBasic, UserLogin, UserCreate, User
from app.users.queries import GET_USERS_EMAIL_AND_PASSWORD, INSERT_USER


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


async def register_user(db_pool: Pool, user: UserCreate):
    try:
        async with db_pool.acquire() as connection:
            parms = (user.email, user.passwd, user.is_active) # parametry przekazywane do placeholderów $1 itd. jako zmienna, żeby nie wymieniać tego w poniższej linii kodu
            await connection.execute(INSERT_USER, *parms)
            #row = await connection.fetchrow(INSERT_USER, *parms) # INSERT_USER jest z queries.py, a user.email, user.passwd, user.is_active to przekazywane wartości do placeholderów w zapytaniu tj. $1, $2, $3
            #return UserBasic(**row)
    except Exception as e:
        print(f"Error registering user: {e}")
        raise
