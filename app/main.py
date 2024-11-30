from fastapi import FastAPI
from app.database import DataBasePool
from app.users.router import users


app = FastAPI()


@app.on_event("startup")
async def startup():
    await DataBasePool.setup()


@app.on_event("shutdown")
async def shutdown():
    await DataBasePool.teardown()


app.include_router(users)
