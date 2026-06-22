from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import uuid

router = APIRouter(prefix="/uuid")


@router.get("/")
def returnUUID():
    return PlainTextResponse(content=str(uuid.uuid4()))
