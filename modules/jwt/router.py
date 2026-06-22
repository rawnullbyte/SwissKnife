from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import jwt

router = APIRouter(prefix="/jwt")


@router.get("/{token:path}")
def hello(token: str):
    try:
        return JSONResponse(
            jwt.decode(
                token,
                options={"verify_signature": False}
            )

        )
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)