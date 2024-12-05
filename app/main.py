import uvicorn
from fastapi import FastAPI, APIRouter
from app.database import DataBasePool

from app.users.router import router as users_router

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")


@app.on_event("startup")
async def startup():
    await DataBasePool.setup()


@app.on_event("shutdown")
async def shutdown():
    await DataBasePool.teardown()


api_router.include_router(users_router, prefix="/users")


app.include_router(api_router)


def run():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
