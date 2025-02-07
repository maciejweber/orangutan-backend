from datetime import datetime
from app.database import execute_db_query
from typing import List


async def create_training_session_in_db(userid: int, trainingid: int) -> dict:

    query = """
        INSERT INTO training_sessions (userid, trainingid, start_time)
        VALUES ($1, $2, NOW())
        RETURNING id, userid, trainingid, start_time, end_time
    """
    result = await execute_db_query(query, userid, trainingid)
    return dict(result[0])


async def end_training_session_in_db(session_id: int, end_time: datetime) -> dict:
    query = """
        UPDATE training_sessions
           SET end_time = $2
         WHERE id = $1
        RETURNING id, userid, trainingid, start_time, end_time
    """
    result = await execute_db_query(query, session_id, end_time)
    if result:
        return dict(result[0])
    return {}


async def get_training_session_by_id(session_id: int) -> dict:
    query = """
        SELECT id, userid, trainingid, start_time, end_time
          FROM training_sessions
         WHERE id = $1
    """
    result = await execute_db_query(query, session_id)
    if result:
        return dict(result[0])
    return {}


async def get_training_by_id(userid: int, trainingid: int) -> dict:
    query = """
        SELECT id, userid, name
          FROM training
         WHERE id = $1
           AND userid = $2
    """
    result = await execute_db_query(query, trainingid, userid)
    return dict(result[0]) if result else {}


async def get_all_series_for_session(session_id: int) -> List[dict]:
    query = """
        SELECT id, userid, exerciseid, trainingid, setnumber, countnumber, weight, insstmp
          FROM series
         WHERE trainingsessionid = $1
         ORDER BY insstmp ASC
    """
    results = await execute_db_query(query, session_id)
    return [dict(r) for r in results]


async def get_completed_sessions_for_user(userid: int) -> List[dict]:
    query = """
        SELECT id, userid, trainingid, start_time, end_time
          FROM training_sessions
         WHERE userid = $1
           AND end_time IS NOT NULL
         ORDER BY end_time DESC
    """
    results = await execute_db_query(query, userid)
    return [dict(r) for r in results]
