from app.database import execute_db_query


async def get_user_trainings_from_db(userid: int):
    query = """
        SELECT id, userid, name
        FROM training
        WHERE userid = $1
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


async def get_training_exercises_from_db(trainingid: int):
    query = """
        SELECT e.id, e.partiesid, e.name, e.image, e.hardrate, e.description, e.serieshint, e.counthint, e.breakhint
        FROM exercises e
        JOIN training_exercises te ON e.id = te.exerciseid
        WHERE te.trainingid = $1
    """
    results = await execute_db_query(query, trainingid)
    return [dict(row) for row in results]
