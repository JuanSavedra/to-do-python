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

@app.get("/tasks", response_model=list[Task])
def read_tasks(con: sqlite3.Connection = Depends(get_endpoint_connection)):
    cur = con.cursor()
    cur.execute("SELECT id, name, description, status FROM Task ORDER BY id ASC")
    rows = cur.fetchall()

    tasks = []
    for row in rows:
        tasks.append(dict(row))

    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, con: sqlite3.Connection = Depends(get_endpoint_connection)):
    cur = con.cursor()
    cur.execute("SELECT id, name, description, status FROM Task WHERE id = ?", (task_id,))
    row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return dict(row)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate, con: sqlite3.Connection = Depends(get_endpoint_connection)):
    cur = con.cursor()

    try:
        cur.execute(
            "UPDATE Task SET name = ?, description = ?, status = ? WHERE id = ?",
            (task.name, task.description, task.status, task_id)
        )

        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        
        con.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Task with this name already exists")

    dict_response = {
        "id": task_id,
        "name": task.name,
        "description": task.description,
        "status": task.status
    }
    
    return dict_response