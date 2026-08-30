# Task API

A small in-memory CRUD API for managing a to-do list, built with **FastAPI**.
This is the FlyRank Internship — Backend Track — Week 2 — Assignment A1 submission.

## What this is

A REST API with full CRUD (Create, Read, Update, Delete) on a list of tasks.
Data is stored **in memory only** — it resets every time the server restarts.
That's intentional at this stage (no database yet — that's next week).

## How to install & run

```bash
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open **http://localhost:8000** in your browser, or **http://localhost:8000/docs**
for the interactive Swagger UI (built in automatically by FastAPI).

## Endpoints

| Method | Path              | Description                          | Success | Errors        |
|--------|-------------------|---------------------------------------|---------|---------------|
| GET    | `/`               | API info                              | 200     | —             |
| GET    | `/health`         | Health check                          | 200     | —             |
| GET    | `/tasks`          | List all tasks (supports `?done=` and `?search=`) | 200 | — |
| GET    | `/tasks/{id}`     | Get one task                          | 200     | 404 if missing |
| POST   | `/tasks`          | Create a task (`{"title": "..."}`)    | 201     | 400 if title missing/empty |
| PUT    | `/tasks/{id}`     | Update a task's title and/or done     | 200     | 400 invalid body, 404 if missing |
| DELETE | `/tasks/{id}`     | Delete a task                         | 204     | 404 if missing |
| GET    | `/stats`          | Task counts (extra)                   | 200     | — |
| POST   | `/reset`          | Reset to the 3 example tasks (extra)  | 200     | — |

## Example curl output

```
$ curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

Screenshot of `/docs` with the full CRUD cycle tested via "Try it out": *(add your screenshot here)*

## The mortality experiment

Restarting the server resets all tasks back to the original 3 examples — anything created,
updated, or deleted during the session is lost. This happens because the data lives only in
a Python list in memory, not on disk or in a database. This is the exact problem Week 3
(databases) solves.

## AI vs me (Stage 7 — bonus)

*(Fill this in after you complete Stage 7: your prompt, what the AI got right/wrong, and
what your prompt forgot to specify.)*
