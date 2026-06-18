from database.mission_db import mdb
from database.agent_db import adb


from fastapi import Body, Query, APIRouter, HTTPException

router = APIRouter()

@router.get("/reports/summary")
def summary():
    pass

@router.get("/reports/missions-by-status")
def missions_by_status():
    pass

@router.get("/reports/top-agent")
def top_agent():
    pass
