"""
Task API — a small CRUD API for managing a to-do list.
Built for FlyRank Internship, Backend Track, Week 2, Assignment A1.
Data lives in memory only — it resets when the server restarts (that's on purpose, see README).
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A small in-memory CRUD API for managing a to-do list.",
)

# ---------------------------------------------------------------------------
# Stage 2: in-memory "database" — just a Python list, pre-filled with 3 tasks
# ---------------------------------------------------------------------------
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Read FastAPI docs", "done": True},
    {"id": 3, "title": "Build the CRUD API", "done": False},
]
next_id = 4  # counter for the next task's id


# Request body shapes (Pydantic validates these automatically)
class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# ---------------------------------------------------------------------------
# Stage 1: root + health endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["meta"], summary="API info")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", tags=["meta"], summary="Health check")
def health_check():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Stage 2: Read
# ---------------------------------------------------------------------------
@app.get("/tasks", tags=["tasks"], summary="List all tasks (optionally filter/search)")
def list_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    result = tasks
    if done is not None:
        result = [t for t in result if t["done"] == done]
    if search:
        result = [t for t in result if search.lower() in t["title"].lower()]
    return result


@app.get("/tasks/{task_id}", tags=["tasks"], summary="Get one task by id")
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---------------------------------------------------------------------------
# Stage 3: Create
# ---------------------------------------------------------------------------
@app.post("/tasks", status_code=201, tags=["tasks"], summary="Create a new task")
def create_task(new_task: TaskCreate):
    global next_id
    if not new_task.title or not new_task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")

    task = {"id": next_id, "title": new_task.title.strip(), "done": False}
    tasks.append(task)
    next_id += 1
    return task


# ---------------------------------------------------------------------------
# Stage 4: Update & Delete
# ---------------------------------------------------------------------------
@app.put("/tasks/{task_id}", tags=["tasks"], summary="Update a task")
def update_task(task_id: int, patch: TaskUpdate):
    for t in tasks:
        if t["id"] == task_id:
            if patch.title is not None:
                if not patch.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                t["title"] = patch.title.strip()
            if patch.done is not None:
                t["done"] = patch.done
            return t
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204, tags=["tasks"], summary="Delete a task")
def delete_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---------------------------------------------------------------------------
# Optional extras (stretch goals)
# ---------------------------------------------------------------------------
@app.get("/stats", tags=["extras"], summary="Task counts")
def stats():
    total = len(tasks)
    done = len([t for t in tasks if t["done"]])
    return {"total": total, "done": done, "open": total - done}


@app.post("/reset", tags=["extras"], summary="Reset to the 3 example tasks")
def reset_tasks():
    global tasks, next_id
    tasks = [
        {"id": 1, "title": "Buy milk", "done": False},
        {"id": 2, "title": "Read FastAPI docs", "done": True},
        {"id": 3, "title": "Build the CRUD API", "done": False},
    ]
    next_id = 4
    return {"status": "reset"}