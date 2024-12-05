from app.database import execute_db_query


async def get_users_from_db():
    return await execute_db_query(
        "SELECT id, email, is_active, insstmp, updstmp FROM users"
    )


async def get_user_details_from_db_by_id(id: int):
    user_details = await execute_db_query(
        "SELECT id, email, is_active, insstmp, updstmp FROM users WHERE id = $1", id
    )
    if user_details:
        return user_details[0]
    return None


async def get_user_details_from_db_by_email(email: str):
    user_details = await execute_db_query(
        "SELECT id, email, is_active, insstmp, updstmp FROM users WHERE email = $1",
        email,
    )
    if user_details:
        return user_details[0]
    return None
