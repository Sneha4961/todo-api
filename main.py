from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Read FastAPI docs", "done": True},
    {"id": 3, "title": "Build the CRUD API", "done": False},
]
next_id = 4


class TaskCreate(BaseModel):
    title: str


@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    global next_id
    if not new_task.title or not new_task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")

    task = {"id": next_id, "title": new_task.title.strip(), "done": False}
    tasks.append(task)
    next_id += 1
    return task