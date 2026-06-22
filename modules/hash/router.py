from __future__ import annotations
from fastapi import APIRouter, Request, HTTPException, status, Query
from fastapi.responses import PlainTextResponse
from enum import Enum
import hashlib

router = APIRouter()

class HashType(str, Enum):
    SHA1 = "sha1"
    SHA224 = "sha224"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"
    SHA3_256 = "sha3_256"
    SHA3_384 = "sha3_384"
    SHA3_512 = "sha3_512"
    SHAKE_128 = "shake_128"
    SHAKE_256 = "shake_256"
    MD5 = "md5"
    ARGON2 = "argon2"

@router.get("/hash")
async def hashRequest(
    request: Request,
    type: HashType = Query(default=None),
    data: str = None,
):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Missing 'data' query parameter"
        )
    elif not type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Missing 'type' query parameter.",
                "available_types": [t.value for t in HashType],
            },
        )
    
    if type == "sha1":
        return PlainTextResponse(hashlib.sha1(data.encode('utf-8')).hexdigest())
    elif type == "sha224":
        return PlainTextResponse(hashlib.sha224(data.encode('utf-8')).hexdigest())
    elif type == "sha256":
        return PlainTextResponse(hashlib.sha256(data.encode('utf-8')).hexdigest())
    elif type == "sha384":
        return PlainTextResponse(hashlib.sha384(data.encode('utf-8')).hexdigest())
    elif type == "sha512":
        return PlainTextResponse(hashlib.sha512(data.encode('utf-8')).hexdigest())
    elif type == "sha3_256":
        return PlainTextResponse(hashlib.sha3_256(data.encode('utf-8')).hexdigest())
    elif type == "sha3_384":
        return PlainTextResponse(hashlib.sha3_384(data.encode('utf-8')).hexdigest())
    elif type == "sha3_512":
        return PlainTextResponse(hashlib.sha3_512(data.encode('utf-8')).hexdigest())
    elif type == "shake_128":
        return PlainTextResponse(hashlib.shake_128(data.encode('utf-8')).hexdigest(32))
    elif type == "shake_256":
        return PlainTextResponse(hashlib.shake_256(data.encode('utf-8')).hexdigest(32))
    elif type == "md5":
        return PlainTextResponse(hashlib.md5(data.encode('utf-8')).hexdigest())