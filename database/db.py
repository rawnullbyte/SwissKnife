from __future__ import annotations

import secrets
import sqlite3
from dataclasses import dataclass
from hashlib import pbkdf2_hmac
from hmac import compare_digest
from pathlib import Path

_ITERATIONS = 600_000

@dataclass(frozen=True)
class User:
    id: int
    username: str


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect("database/swissknife.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = pbkdf2_hmac("sha256", password.encode(), salt.encode(), _ITERATIONS)
    return f"pbkdf2_sha256${_ITERATIONS}${salt}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt, digest = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        candidate = pbkdf2_hmac("sha256", password.encode(), salt.encode(), int(iterations))
    except (ValueError, TypeError):
        return False

    return compare_digest(candidate.hex(), digest)


def create_user(username: str, password: str) -> User:
    init_db()
    with _connect() as conn:
        cursor = conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password)),
        )
        return User(id=int(cursor.lastrowid), username=username)


def authenticate_user(username: str, password: str) -> User | None:
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if row is None:
        return None
    if not verify_password(password, str(row["password_hash"])):
        return None
    return User(id=int(row["id"]), username=str(row["username"]))


def get_user(user_id: int) -> User | None:
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, username FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

    if row is None:
        return None
    return User(id=int(row["id"]), username=str(row["username"]))
