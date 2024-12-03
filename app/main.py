from fastapi import FastAPI
from app.database import DataBasePool
from app.users.router import users
import uvicorn

app = FastAPI()


@app.on_event("startup")
async def startup():
    await DataBasePool.setup()


@app.on_event("shutdown")
async def shutdown():
    await DataBasePool.teardown()


app.include_router(users)


def run():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
