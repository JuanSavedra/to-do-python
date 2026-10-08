import sqlite3
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from app.database import get_endpoint_connection, init_db
from app.schemas import Task, TaskCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate, con: sqlite3.Connection = Depends(get_endpoint_connection)):
    cur = con.cursor()

    try:
        cur.execute(
            "INSERT INTO Task (name, description, status) VALUES (?, ?, ?)",
            (task.name, task.description, task.status)
        )
        con.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Task with this name already exists")

    dict_response = {
        "id": cur.lastrowid,
        "name": task.name,
        "description": task.description,
        "status": task.status
    }

    return dict_response