from app.database import execute_db_query


# async def get_user_trainings_from_db(userid: int):
#     query = """
#         SELECT id, userid, name
#         FROM training
#         WHERE userid = $1
#     """
#     results = await execute_db_query(query, userid)
#     return [dict(row) for row in results]


async def get_user_trainings_from_db(userid: int):
    query = """
        SELECT 
            t.id, 
            t.userid, 
            t.name, 
            COALESCE(COUNT(te.id), 0) AS "exercisesNumber"
        FROM training t
        LEFT JOIN training_exercises te
               ON t.id = te.trainingid
        WHERE t.userid = $1
        GROUP BY t.id
    """
    results = await execute_db_query(query, userid)
    return [dict(row) for row in results]


async def create_training_in_db(userid: int, name: str):
    query = """
        INSERT INTO training (userid, name)
        VALUES ($1, $2)
        RETURNING id, userid, name
    """
    result = await execute_db_query(query, userid, name)
    return dict(result[0])


async def add_training_exercise_in_db(
    userid: int,
    trainingid: int,
    exerciseid: int,
    minsetnumber: int = None,
    maxsetnumber: int = None,
):
    # query = """
    #     INSERT INTO training_exercises (userid, trainingid, exerciseid, minsetnumber, maxsetnumber)
    #     VALUES ($1, $2, $3, $4, $5)
    #     RETURNING id, userid, trainingid, exerciseid, minsetnumber, maxsetnumber
    # """
    query = """
        INSERT INTO training_exercises (userid, trainingid, exerciseid)
        VALUES ($1, $2, $3)
        RETURNING id, userid, trainingid, exerciseid
    """
    result = await execute_db_query(query, userid, trainingid, exerciseid)
    return dict(result[0])


async def delete_training_exercise_from_db(
    userid: int, trainingid: int, exerciseid: int
):
    query = """
        DELETE FROM training_exercises 
        WHERE userid = $1 AND trainingid = $2 AND exerciseid = $3
        RETURNING id, userid, trainingid, exerciseid
    """
    results = await execute_db_query(query, userid, trainingid, exerciseid)
    if results:
        return dict(results[0])
    else:
        return None


async def get_training_exercises_from_db(trainingid: int):
    query = """
        SELECT e.id, e.partiesid, e.name, e.hardrate, e.description, e.serieshint, e.counthint, e.breakhint
        FROM exercises e
        JOIN training_exercises te ON e.id = te.exerciseid
        WHERE te.trainingid = $1
    """
    # query = """
    #     SELECT e.id, e.partiesid, e.name, e.image, e.hardrate, e.description, e.serieshint, e.counthint, e.breakhint
    #     FROM exercises e
    #     JOIN training_exercises te ON e.id = te.exerciseid
    #     WHERE te.trainingid = $1
    # """
    results = await execute_db_query(query, trainingid)
    return [dict(row) for row in results]


async def delete_all_exercises_for_training_from_db(trainingid: int):
    query = """
        DELETE FROM training_exercises
        WHERE trainingid = $1
        RETURNING id
    """
    result = await execute_db_query(query, trainingid)
    return [dict(row) for row in result]


async def delete_training_from_db(userid: int, trainingid: int):
    query = """
        DELETE FROM training
        WHERE userid = $1 AND id = $2
        RETURNING id, userid, name
    """
    result = await execute_db_query(query, userid, trainingid)
    if result:
        return dict(result[0])
    else:
        return None
