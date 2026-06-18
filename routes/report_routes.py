from database.mission_db import mdb
from database.agent_db import adb

from fastapi import Body, Query, APIRouter, HTTPException

router = APIRouter()

@router.get("/reports/summary")
def summary():
    if not adb.get_all_agents() or not mdb.get_all_missions():
        return {"active_agents_count": 0,
                "total_missions": 0,
                "open_missions": 0,
                "completed_missions": 0,
                "failed_missions": 0,
                "critical_missions": 0}
    
    return {
            "active_agents_count": adb.count_active_agents(),
            "total_missions": len(mdb.get_all_missions()),
            "open_missions": mdb.count_open_missions(),
            "completed_missions": mdb.count_by_status('COMPLETED'),
            "failed_missions": mdb.count_by_status('FAILED'),
            "critical_missions": mdb.count_critical_missions()
            }
    

@router.get("/reports/missions-by-status")
def missions_by_status():
    if not adb.get_all_agents() or not mdb.get_all_missions():
        return {"open": 0,"in_progress": 0,"completed": 0,"failed": 0,"cancelled": 0}
    return {
            "open": mdb.count_open_missions(),
            "in_progress": mdb.count_by_status("IN_PROGRESS"),
            "completed": mdb.count_by_status("COMPLETED"),
            "failed": mdb.count_by_status("FAILED"),
            "critical": mdb.count_by_status("CRITICAL")
            }


@router.get("/reports/top-agent")
def top_agent():
    if not adb.get_all_agents():
        raise HTTPException(404, "No agents")
    return mdb.get_top_agent()
