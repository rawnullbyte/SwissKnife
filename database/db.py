from __future__ import annotations

import secrets
import sqlite3
import uuid
from dataclasses import dataclass
from hashlib import pbkdf2_hmac
from hmac import compare_digest

_ITERATIONS = 600_000

@dataclass(frozen=True)
class User:
    id: str
    username: str


@dataclass(frozen=True)
class Paste:
    id: str
    owner_id: str
    content: str
    visibility: str
    created_at: str


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect("database/swissknife.sqlite3")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _new_user_id() -> str:
    return str(uuid.uuid4())


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pastes (
                id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                content TEXT NOT NULL,
                visibility TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE CASCADE
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
    user_id = _new_user_id()
    with _connect() as conn:
        conn.execute(
            "INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)",
            (user_id, username, hash_password(password)),
        )
        return User(id=user_id, username=username)


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
    return User(id=str(row["id"]), username=str(row["username"]))


def get_user(user_id: str) -> User | None:
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, username FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

    if row is None:
        return None
    return User(id=str(row["id"]), username=str(row["username"]))


def _row_to_paste(row: sqlite3.Row) -> Paste:
    return Paste(
        id=str(row["id"]),
        owner_id=str(row["owner_id"]),
        content=str(row["content"]),
        visibility=str(row["visibility"]),
        created_at=str(row["created_at"]),
    )


def create_paste(owner_id: str, content: str, visibility: str) -> Paste:
    init_db()
    paste_id = str(uuid.uuid4())
    with _connect() as conn:
        conn.execute(
            "INSERT INTO pastes (id, owner_id, content, visibility) VALUES (?, ?, ?, ?)",
            (paste_id, owner_id, content, visibility),
        )
        row = conn.execute(
            "SELECT id, owner_id, content, visibility, created_at FROM pastes WHERE id = ?",
            (paste_id,), # comma after paste_id because (x) == x, not a tupple, (x,) makes it a tupple
        ).fetchone()
    assert row is not None
    return _row_to_paste(row)


def list_pastes(owner_id: str, page: int, only_own: bool, per_page: int = 25) -> list[Paste]:
    init_db()
    offset = (page - 1) * per_page # -1 because we count from 0 and not 1, so page 1 = entries 0-25
    with _connect() as conn:
        if only_own:
            rows = conn.execute(
                "SELECT id, owner_id, content, visibility, created_at FROM pastes WHERE owner_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (owner_id, per_page, offset),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, owner_id, content, visibility, created_at FROM pastes WHERE visibility = 'public' OR owner_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (owner_id, per_page, offset),
            ).fetchall()
    return [_row_to_paste(row) for row in rows]


def get_paste(owner_id: str, paste_id: str) -> Paste | None:
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, owner_id, content, visibility, created_at FROM pastes WHERE id = ? AND (owner_id = ? OR visibility IN ('public', 'unlisted'))",
            (paste_id, owner_id),
        ).fetchone()
    if row is None:
        return None
    return _row_to_paste(row)


def delete_paste(owner_id: str, paste_id: str) -> bool:
    init_db()
    with _connect() as conn:
        cursor = conn.execute(
            "DELETE FROM pastes WHERE id = ? AND owner_id = ?",
            (paste_id, owner_id),
        )
    return cursor.rowcount > 0
