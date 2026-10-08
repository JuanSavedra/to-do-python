from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import get_endpoint_connection, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}