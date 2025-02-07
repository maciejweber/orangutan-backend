from fastapi import APIRouter, Depends
from typing import List
from app.dependencies.auth import get_current_user
from app.users.models import User
from app.training_sessions.models import (
    TrainingSession,
    CreateTrainingSessionRequest,
    EndTrainingSessionRequest,
)
from app.training_sessions.services import (
    create_new_session,
    end_session,
    get_completed_sessions,
    get_session_summary,
)

router = APIRouter()


@router.post("", response_model=TrainingSession)
async def start_training_session(
    request: CreateTrainingSessionRequest,
    current_user: User = Depends(get_current_user),
):
    session = await create_new_session(current_user.id, request)
    return session


@router.patch("/{session_id}", response_model=TrainingSession)
async def finish_training_session(
    session_id: int,
    request: EndTrainingSessionRequest = EndTrainingSessionRequest(),
    current_user: User = Depends(get_current_user),
):
    session = await end_session(current_user.id, session_id, request)
    return session


@router.get("/{session_id}/summary")
async def get_training_session_summary(
    session_id: int, current_user: User = Depends(get_current_user)
):
    summary = await get_session_summary(current_user.id, session_id)
    return summary


@router.get("/completed", response_model=List[TrainingSession])
async def get_completed_training_sessions(
    current_user: User = Depends(get_current_user),
):
    sessions = await get_completed_sessions(current_user.id)
    return sessions
