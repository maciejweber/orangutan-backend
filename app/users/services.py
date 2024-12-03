from asyncpg import Pool
from app.users.queries import GET_USERS
from app.users.models import User


async def get_users(db_pool: Pool):
    async with db_pool.acquire() as connection:
        users: User = await connection.fetch(GET_USERS)
        return [User(**dict(user)) for user in users]
