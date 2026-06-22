from __future__ import annotations

import secrets
import sqlite3
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field

from database.db import User, authenticate_user, create_user, get_user, init_db

router = APIRouter(prefix="/auth", tags=["auth"])
_sessions: dict[str, str] = {}


class Credentials(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=256)


class UserResponse(BaseModel):
    id: str
    username: str


class TokenResponse(BaseModel):
    token: str
    user: UserResponse


def _user_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, username=user.username)


def _issue_token(user: User) -> TokenResponse:
    token = secrets.token_urlsafe(32)
    _sessions[token] = user.id
    return TokenResponse(token=token, user=_user_response(user))


def _current_user(authorization: Annotated[str | None, Header()] = None) -> User:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    token = authorization.removeprefix("Bearer ").strip()
    user_id = _sessions.get(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token",
        )

    user = get_user(user_id)
    if user is None:
        _sessions.pop(token, None)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token",
        )

    return user


@router.on_event("startup")
def startup() -> None:
    init_db()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(credentials: Credentials) -> TokenResponse:
    try:
        user = create_user(credentials.username, credentials.password)
    except sqlite3.IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        ) from exc

    return _issue_token(user)


@router.post("/login")
def login(credentials: Credentials) -> TokenResponse:
    user = authenticate_user(credentials.username, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return _issue_token(user)


@router.get("/account")
def account(authorization: Annotated[str | None, Header()] = None) -> UserResponse:
    return _user_response(_current_user(authorization))
