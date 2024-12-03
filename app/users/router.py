from fastapi import APIRouter, Depends, HTTPException
import asyncpg
from app.database import DataBasePool
from app.users.services import get_users, authenticate_user, register_user, get_exercises, register_plan
from app.users.models import UserLogin, UserCreate, User, UserBasic, MessageResponse, TrainingCreate


users = APIRouter()


@users.get("/users")
async def get_users_endpoint(db_pool: asyncpg.Pool = Depends(DataBasePool.get_pool)):
    users = await get_users(db_pool)
    return users


@users.post("/login")
async def login_endpoint(login_request: UserLogin, db_pool: asyncpg.Pool = Depends(DataBasePool.get_pool)):
    user = await authenticate_user(db_pool, login_request.email, login_request.passwd)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user


@users.post("/register", response_model=MessageResponse)
async def register_endpoint(user_create: UserCreate, db_pool: asyncpg.Pool = Depends(DataBasePool.get_pool)):
    existing_user = await db_pool.fetchval("SELECT COUNT(1) FROM users WHERE email = $1", user_create.email) # wyszukanie wierszy z users o przekazywanym przy rejestracji mailu
    if existing_user > 0: # sprawdzenie czy istnieje więcej niż 1 taki mail
        raise HTTPException(status_code=400, detail="Email already in use")
    #new_user = await register_user(db_pool, user_create) # wywołanie funkcji register_user i przekazanie 2 argumentów tj. db_pool czyli połączenia z puli połaczeń do bazy oraz user_create czyli obiektu, który jest instancją UserCreate w models.py. UserCreate zawiera dane potrzebne do utworzenia nowego użytkownika
    #return new_user
    await register_user(db_pool, user_create)
    return {"message": "User registered successfully"}


@users.get("/exercises")
async def get_exercises_endpoint(partiesid: int, db_pool: asyncpg.Pool = Depends(DataBasePool.get_pool)): # partiesid to parametr w argumencie endpointu przekazywany do funkcji get_exercises
    exercises = await get_exercises(db_pool, partiesid)
    return exercises


@users.post("/register_training", response_model=MessageResponse)
async def register_training_endpoint(training_create: TrainingCreate, db_pool: asyncpg.Pool = Depends(DataBasePool.get_pool)):
    existing_plan = await db_pool.fetchval("SELECT COUNT(1) FROM training WHERE userid = $1 and name = $2", training_create.userid, training_create.name)
    if existing_plan > 0:
        raise HTTPException(status_code=400, detail="Training already exists")
    await register_plan(db_pool, training_create)
    return {"message": "Training registered successfully"}

