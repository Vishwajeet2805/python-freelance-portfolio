# FastAPI Task Management API

A portfolio-ready REST API for creating, reading, updating, filtering, and deleting tasks.

## Features

- RESTful CRUD endpoints
- SQLite database
- Pydantic request validation
- Error handling
- Task priority validation
- Completed-task filtering
- Interactive Swagger API documentation
- Clean project structure

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLite
- Uvicorn

## Project Structure

```text
fastapi-task-manager/
├── app/
│   ├── __init__.py
│   └── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Create and activate a virtual environment if desired:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Health check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List/filter tasks |
| GET | `/tasks/{id}` | Get one task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Example Request

### POST `/tasks`

```json
{
  "title": "Finish Python portfolio",
  "description": "Prepare GitHub projects",
  "priority": "high"
}
```

### Example Response

```json
{
  "id": 1,
  "title": "Finish Python portfolio",
  "description": "Prepare GitHub projects",
  "priority": "high",
  "completed": false
}
```

## Filtering

Get only incomplete tasks:

```text
GET /tasks?completed=false
```

Get high-priority tasks:

```text
GET /tasks?priority=high
```

Combine filters:

```text
GET /tasks?completed=false&priority=high
```

## Portfolio Highlights

This project demonstrates:

- API design
- CRUD operations
- Database integration
- Input validation
- HTTP status codes
- Exception handling
- Query filtering
- Backend architecture

## Security Note

This demo intentionally uses SQLite and has no authentication layer. Do not use it as-is for production systems handling sensitive data.

## License

MIT
