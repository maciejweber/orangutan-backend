from app.database import execute_db_query


async def add_series_in_db(
    userid: int,
    trainingid: int,
    exerciseid: int,
    setnumber: int,
    countnumber: int,
    weight: float,
    trainingsessionid: int,
):
    query = """
        INSERT INTO series (userid, trainingid, exerciseid, setnumber, countnumber, weight, trainingsessionid)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id, userid, trainingid, exerciseid, setnumber, countnumber, weight, insstmp, trainingsessionid
    """
    result = await execute_db_query(
        query,
        userid,
        trainingid,
        exerciseid,
        setnumber,
        countnumber,
        weight,
        trainingsessionid,
    )
    return dict(result[0])


async def get_training_by_id(userid: int, trainingid: int):
    query = """
        SELECT id, userid, name
        FROM training
        WHERE id = $1 AND userid = $2
    """
    results = await execute_db_query(query, trainingid, userid)
    return dict(results[0]) if results else None


async def get_exercise_in_training(userid: int, trainingid: int, exerciseid: int):
    query = """
        SELECT te.exerciseid
        FROM training_exercises te
        JOIN training t ON te.trainingid = t.id
        WHERE te.trainingid = $1 AND te.exerciseid = $2 AND t.userid = $3
    """
    results = await execute_db_query(query, trainingid, exerciseid, userid)
    return dict(results[0]) if results else None
