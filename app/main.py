from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routers import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
