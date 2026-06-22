from fastapi import APIRouter, Response, HTTPException
import uvicorn.protocols.http.h11_impl
import h11._util

router = APIRouter(prefix="/http")

@router.get("/{code}")
def returnStatusCode(code: int = 200):
    if not 200 <= code <= 1000:
        raise HTTPException(detail="Status code must be between 200 and 1000!", status_code=400)
        
    if code not in uvicorn.protocols.http.h11_impl.STATUS_PHRASES:
        uvicorn.protocols.http.h11_impl.STATUS_PHRASES[code] = b""
    return Response(status_code=code)
