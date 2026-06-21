from fastapi import APIRouter

router = APIRouter(prefix="/hello", tags=["hello"])


@router.get("")
def hello() -> dict[str, str]:
    return {"message": "Hello, World!"}
