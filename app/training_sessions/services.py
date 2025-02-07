from datetime import datetime
from fastapi import HTTPException
from typing import Dict, Any, List, Optional

from app.training_sessions.repositories import (
    create_training_session_in_db,
    end_training_session_in_db,
    get_training_session_by_id,
    get_training_by_id,
    get_all_series_for_session,
    get_completed_sessions_for_user,
    get_last_session,
)
from app.training_sessions.models import (
    TrainingSession,
    CreateTrainingSessionRequest,
    EndTrainingSessionRequest,
)


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

    session_db = await get_training_session_by_id(session_id)
    if not session_db:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session_db["userid"] != userid:
        raise HTTPException(status_code=403, detail="You do not own this session.")

    series_data = await get_all_series_for_session(session_id)
    total_series = len(series_data)
    total_reps = sum(s["countnumber"] for s in series_data)
    total_weight = sum(s["weight"] for s in series_data)

    start_time = session_db["start_time"]
    end_time = session_db["end_time"]
    duration_minutes = None
    if end_time:
        duration_minutes = (end_time - start_time).total_seconds() / 60.0

    average_reps = total_reps / total_series if total_series > 0 else 0

    summary = {
        "session_id": session_id,
        "trainingid": session_db["trainingid"],
        "start_time": start_time,
        "end_time": end_time,
        "total_series": total_series,
        "total_reps": total_reps,
        "total_weight": total_weight,
        "duration_minutes": duration_minutes,
        "average_reps_per_series": average_reps,
    }

    last_session_db = await get_last_session(
        userid=userid,
        trainingid=session_db["trainingid"],
        exclude_session_id=session_id,
    )
    if last_session_db:

        last_series_data = await get_all_series_for_session(last_session_db["id"])
        last_total_series = len(last_series_data)
        last_total_reps = sum(s["countnumber"] for s in last_series_data)
        last_total_weight = sum(s["weight"] for s in last_series_data)

        last_duration_minutes = None
        if last_session_db["end_time"]:
            last_duration_minutes = (
                last_session_db["end_time"] - last_session_db["start_time"]
            ).total_seconds() / 60.0

        last_average_reps = (
            last_total_reps / last_total_series if last_total_series > 0 else 0
        )

        diff_series = total_series - last_total_series
        diff_reps = total_reps - last_total_reps
        diff_weight = total_weight - last_total_weight
        diff_duration = None
        if duration_minutes is not None and last_duration_minutes is not None:
            diff_duration = duration_minutes - last_duration_minutes

        summary["comparison"] = {
            "last_session": {
                "session_id": last_session_db["id"],
                "total_series": last_total_series,
                "total_reps": last_total_reps,
                "total_weight": last_total_weight,
                "duration_minutes": last_duration_minutes,
                "average_reps_per_series": last_average_reps,
            },
            "differences": {
                "series": diff_series,
                "reps": diff_reps,
                "weight": diff_weight,
                "duration_minutes": diff_duration,
            },
        }

    return summary


async def get_completed_sessions(userid: int) -> List[TrainingSession]:
    sessions_data = await get_completed_sessions_for_user(userid)
    return [TrainingSession(**session) for session in sessions_data]
