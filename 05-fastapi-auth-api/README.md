# Secure User Authentication API

A portfolio-ready FastAPI backend demonstrating registration, password hashing, login sessions, protected profile access, and logout.

## Features

- User registration
- Email validation
- Password length validation
- PBKDF2 password hashing with unique salts
- Bearer-token sessions
- Token expiry
- Protected `/users/me` endpoint
- Logout / session revocation
- SQLite persistence
- HTTP error handling
- Swagger documentation

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLite
- Uvicorn
- Standard-library cryptography primitives

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/register` | Create account |
| POST | `/login` | Authenticate |
| GET | `/users/me` | Protected profile |
| POST | `/logout` | Revoke session |

## Example Registration

```json
{
  "email": "demo@example.com",
  "password": "StrongPass123"
}
```

## Example Login

```json
{
  "email": "demo@example.com",
  "password": "StrongPass123"
}
```

The login response contains a bearer token. Use it in Swagger's **Authorize** button to access `/users/me`.

## Security Notes

This is an educational portfolio project, not a production identity service. Production applications should use a mature authentication/security library or managed identity provider, HTTPS, secure secret management, rate limiting, account recovery, email verification, audit logging, and additional threat protections.

No real credentials or secrets are included in this repository.

## Portfolio Highlights

This project demonstrates backend API design, authentication flows, password hashing, session management, validation, protected routes, database persistence, and HTTP error handling.
