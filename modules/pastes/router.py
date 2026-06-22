from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from database import db
from modules.auth.router import _current_user

router = APIRouter(prefix="/pastes")


class PasteCreate(BaseModel):
    content: str = Field(min_length=1, max_length=100_000)
    visibility: str = Field(min_length=1, max_length=16, pattern=r"^(public|private|unlisted)$")


class PasteResponse(BaseModel):
    id: str
    owner_id: str
    content: str
    visibility: str
    created_at: str


@router.get("/", response_model=list[PasteResponse])
def get_pastes(
    user: Annotated[db.User, Depends(_current_user)],
    page: Annotated[int, Query(ge=1)] = 1,
    only_own: Annotated[bool, Query()] = False,
) -> list[PasteResponse]:
    return db.list_pastes(owner_id=user.id, page=page, only_own=only_own)

@router.post("/", response_model=PasteResponse, status_code=status.HTTP_201_CREATED)
def add_paste(
    user: Annotated[db.User, Depends(_current_user)],
    paste: PasteCreate,
) -> PasteResponse:
    return db.create_paste(owner_id=user.id, content=paste.content, visibility=paste.visibility)

@router.get("/{paste_id}", response_model=PasteResponse)
def get_paste(
    user: Annotated[db.User, Depends(_current_user)],
    paste_id: str,
) -> PasteResponse:
    paste = db.get_paste(owner_id=user.id, paste_id=paste_id)
    if paste == None:
        raise HTTPException(status_code=404, detail="Paste not found!")
    if paste.visibility == "private" and user.id != paste.owner_id:
        raise HTTPException(status_code=404, detail="Paste not found!")
    return paste

@router.delete("/{paste_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paste(
    user: Annotated[db.User, Depends(_current_user)],
    paste_id: str,
) -> None:
    paste = db.get_paste(owner_id=user.id, paste_id=paste_id)
    if paste == None:
        raise HTTPException(status_code=404, detail="Paste not found!")
    if paste.visibility == "private" and user.id != paste.owner_id:
        raise HTTPException(status_code=404, detail="Paste not found!")
    return db.delete_paste(owner_id=user.id, paste_id=paste_id)