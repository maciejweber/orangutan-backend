from asyncpg import Pool
from app.users.queries import GET_USERS
from app.users.models import User
from app.database import execute_db_query


async def get_users():
    users = await execute_db_query(GET_USERS)
    return [User(**dict(user)) for user in users]
