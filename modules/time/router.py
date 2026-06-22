from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones
from datetime import datetime

router = APIRouter(prefix="/time")

@router.get("/", response_class=JSONResponse)
def get_all_timezones():
    return sorted(list(available_timezones()))

@router.get("/{tz:path}")
def timeInTimezone(tz: str):
    query = tz.lower()
    matches = [zone for zone in available_timezones() if query in zone.lower()]

    if not matches:
        raise HTTPException(
            status_code=404, 
            detail=f"Timezone matching '{tz}' not found."
        )

    if len(matches) > 1:
        raise HTTPException(
            status_code=400, 
            detail=f"Multiple timezones found matching '{tz}': {matches}. Please be more specific."
        )

    local_time = datetime.now(ZoneInfo(matches[0]))
    time_str = local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    return PlainTextResponse(content=time_str)