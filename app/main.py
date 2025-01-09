import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from app.database import DataBasePool

from app.users.router import router as users_router
from app.exercises.router import router as exercises_router
from app.trainings.router import router as trainings_router

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

ORANGUTAN_ASCII = r"""
__________________AAAA_______________AAAA______________________
                  VVVV               VVVV
                  (__)               (__)
                   \ \               / /
                    \ \   \\|||//   / /
                     > \ \   _   _   / <
                      > \ / \ / \ / <
                       > \\_o_o_// <
                        > ( (_) ) <
                         >|     |<
                        / |\___/| \\
                        / (_____) \\
                        /         \\
                         /   o   \\
                          ) ___ (
                         / /   \ \\
                        ( /     \ )
                        ><       ><
                       ///\     /\\
                       '''       '''        
"""


@app.on_event("startup")
async def startup():
    await DataBasePool.setup()


@app.on_event("shutdown")
async def shutdown():
    await DataBasePool.teardown()


@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = f"""
    <html>
        <head>
            <title>Orangutan</title>
        </head>
        <body>
            <pre>{ORANGUTAN_ASCII}</pre>
        </body>
    </html>
    """
    return html_content


api_router.include_router(users_router, prefix="/users")
api_router.include_router(exercises_router, prefix="/exercises")
api_router.include_router(trainings_router, prefix="/trainings")

app.include_router(api_router)


def run():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
