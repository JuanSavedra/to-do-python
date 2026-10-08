from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    name: str
    description: str | None = None
    status: int = Field(0, ge=0, le=1, description="Status must be between 0 and 1")

class Task(TaskCreate):
    id: int