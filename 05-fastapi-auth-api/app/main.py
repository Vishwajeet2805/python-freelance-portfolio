from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os
import secrets
import sqlite3

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

DATABASE = "users.db"
TOKEN_TTL_HOURS = 24
app = FastAPI(
    title="Secure User Authentication API",
    description="Portfolio-ready authentication API with hashed passwords and bearer tokens.",
    version="1.0.0"
)


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token_hash TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    connection.commit()
    connection.close()


initialize_database()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: str


def hash_password(password: str, salt: bytes | None = None):
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        200_000
    )
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password: str, stored_hash: str):
    try:
        salt_hex, digest_hex = stored_hash.split("$", 1)
        salt = bytes.fromhex(salt_hex)
        calculated = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            200_000
        ).hex()
        return hmac.compare_digest(calculated, digest_hex)
    except ValueError:
        return False


def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()


def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid bearer token."
        )

    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token.")

    connection = get_connection()
    session = connection.execute(
        "SELECT * FROM sessions WHERE token_hash = ?",
        (hash_token(token),)
    ).fetchone()

    if session is None:
        connection.close()
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    expires_at = datetime.fromisoformat(session["expires_at"])
    if expires_at <= datetime.now(timezone.utc):
        connection.execute(
            "DELETE FROM sessions WHERE token_hash = ?",
            (hash_token(token),)
        )
        connection.commit()
        connection.close()
        raise HTTPException(status_code=401, detail="Token expired.")

    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()
    connection.close()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")

    return user


@app.get("/")
def root():
    return {"message": "Authentication API is running", "docs": "/docs"}


@app.post("/register", status_code=201)
def register(data: RegisterRequest):
    email = data.email.lower()
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (email, password_hash, created_at)
            VALUES (?, ?, ?)
            """,
            (
                email,
                hash_password(data.password),
                datetime.now(timezone.utc).isoformat()
            )
        )
        connection.commit()

        return {
            "id": cursor.lastrowid,
            "email": email,
            "message": "User registered successfully."
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists."
        )
    finally:
        connection.close()


@app.post("/login")
def login(data: LoginRequest):
    connection = get_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (data.email.lower(),)
    ).fetchone()

    if user is None or not verify_password(
        data.password, user["password_hash"]
    ):
        connection.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=TOKEN_TTL_HOURS)

    connection.execute(
        """
        INSERT INTO sessions (token_hash, user_id, expires_at)
        VALUES (?, ?, ?)
        """,
        (hash_token(token), user["id"], expires.isoformat())
    )
    connection.commit()
    connection.close()

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_at": expires.isoformat()
    }


@app.get("/users/me", response_model=ProfileResponse)
def profile(user=Depends(get_current_user)):
    return {
        "id": user["id"],
        "email": user["email"],
        "created_at": user["created_at"]
    }


@app.post("/logout")
def logout(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token.")

    token = authorization.split(" ", 1)[1].strip()
    connection = get_connection()
    connection.execute(
        "DELETE FROM sessions WHERE token_hash = ?",
        (hash_token(token),)
    )
    connection.commit()
    connection.close()

    return {"message": "Logged out successfully."}
