from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import secrets
import string

router = APIRouter(prefix="/password")

@router.get("/")
def generatePassword():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for _ in range(16):
        password += secrets.choice(chars)

    return PlainTextResponse(password)
