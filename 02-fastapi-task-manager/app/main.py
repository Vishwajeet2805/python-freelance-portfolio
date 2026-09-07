from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
import sqlite3

DATABASE = "tasks.db"

app = FastAPI(
    title="Task Management API",
    description="A portfolio-ready REST API built with FastAPI and SQLite.",
    version="1.0.0"
)


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'medium',
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    connection.commit()
    connection.close()


initialize_database()


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    priority: str = Field(default="medium")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Optional[str] = None
    completed: Optional[bool] = None


def validate_priority(priority: str):
    if priority not in {"low", "medium", "high"}:
        raise HTTPException(
            status_code=400,
            detail="Priority must be low, medium, or high."
        )


def task_response(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "priority": row["priority"],
        "completed": bool(row["completed"])
    }


@app.get("/")
def root():
    return {
        "message": "Task Management API is running",
        "docs": "/docs"
    }


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    validate_priority(task.priority)

    connection = get_connection()
    cursor = connection.execute(
        """
        INSERT INTO tasks (title, description, priority)
        VALUES (?, ?, ?)
        """,
        (task.title.strip(), task.description.strip(), task.priority)
    )
    connection.commit()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    connection.close()
    return task_response(row)


@app.get("/tasks")
def get_tasks(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100)
):
    if priority:
        validate_priority(priority)

    query = "SELECT * FROM tasks WHERE 1=1"
    parameters = []

    if completed is not None:
        query += " AND completed = ?"
        parameters.append(int(completed))

    if priority:
        query += " AND priority = ?"
        parameters.append(priority)

    query += " ORDER BY id DESC LIMIT ?"
    parameters.append(limit)

    connection = get_connection()
    rows = connection.execute(query, parameters).fetchall()
    connection.close()

    return [task_response(row) for row in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()
    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found.")

    return task_response(row)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    connection = get_connection()

    existing = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if existing is None:
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found.")

    data = task.model_dump(exclude_unset=True)

    if "priority" in data:
        validate_priority(data["priority"])

    if "title" in data:
        data["title"] = data["title"].strip()

    if "description" in data:
        data["description"] = data["description"].strip()

    if data:
        fields = []
        values = []

        for field, value in data.items():
            if field == "completed":
                value = int(value)
            fields.append(f"{field} = ?")
            values.append(value)

        values.append(task_id)

        connection.execute(
            f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?",
            values
        )
        connection.commit()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()
    return task_response(row)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found.")

    return {"message": "Task deleted successfully."}
