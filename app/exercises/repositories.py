from app.database import execute_db_query


async def get_all_exercises_from_db():
    query = """
        SELECT 
            id, partiesid, name, image, hardrate, description, serieshint, counthint, breakhint
        FROM exercises
    """
    results = await execute_db_query(query)
    return [dict(row) for row in results]
