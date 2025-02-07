from datetime import datetime
from fastapi import HTTPException
from app.training_sessions.repositories import (
    create_training_session_in_db,
    end_training_session_in_db,
    get_training_session_by_id,
    get_training_by_id,
    get_all_series_for_session,
    get_completed_sessions_for_user,
)
from app.training_sessions.models import (
    TrainingSession,
    CreateTrainingSessionRequest,
    EndTrainingSessionRequest,
)
from typing import Dict, Any, List


async def create_new_session(
    userid: int, request: CreateTrainingSessionRequest
) -> TrainingSession:
    training = await get_training_by_id(userid, request.trainingid)
    if not training:
        raise HTTPException(
            status_code=404, detail="Training not found or not owned by user."
        )

    new_session_db = await create_training_session_in_db(userid, request.trainingid)
    return TrainingSession(**new_session_db)


async def end_session(
    userid: int, session_id: int, request: EndTrainingSessionRequest
) -> TrainingSession:
    session_db = await get_training_session_by_id(session_id)
    if not session_db:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session_db["userid"] != userid:
        raise HTTPException(status_code=403, detail="You do not own this session.")

    end_time = datetime.now()

    updated_db = await end_training_session_in_db(session_id, end_time)
    if not updated_db:
        raise HTTPException(
            status_code=404, detail="Cannot update session or session not found."
        )

    return TrainingSession(**updated_db)


async def get_session_summary(userid: int, session_id: int) -> Dict[str, Any]:
    # 1. Pobierz sesję
    session_db = await get_training_session_by_id(session_id)
    if not session_db:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session_db["userid"] != userid:
        raise HTTPException(status_code=403, detail="You do not own this session.")

    # 2. Pobierz wszystkie serie z 'series' dla trainingsessionid = session_id
    series_data = await get_all_series_for_session(session_id)

    # 3. Policz statystyki:
    total_series = len(series_data)
    total_reps = sum(s["countnumber"] for s in series_data)
    total_weight = sum(s["weight"] for s in series_data)
    # ewentualnie zgrupuj po exerciseid

    return {
        "session_id": session_id,
        "trainingid": session_db["trainingid"],
        "start_time": session_db["start_time"],
        "end_time": session_db["end_time"],
        "total_series": total_series,
        "total_reps": total_reps,
        "total_weight": total_weight,
        # ewentualnie "series": series_data,
    }


async def get_completed_sessions(userid: int) -> List[TrainingSession]:
    sessions_data = await get_completed_sessions_for_user(userid)
    return [TrainingSession(**session) for session in sessions_data]
