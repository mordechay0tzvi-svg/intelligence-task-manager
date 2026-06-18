from database.mission_db import mdb
from database.agent_db import adb
from fastapi import Body, Query, APIRouter, HTTPException
from logs.logger import logger

router = APIRouter()

@router.get("/reports/summary")
def summary():
    logger.info("attempt to get summary")
    if not adb.get_all_agents() or not mdb.get_all_missions():
        logger.info("no data")
        return {"active_agents_count": 0,
                "total_missions": 0,
                "open_missions": 0,
                "completed_missions": 0,
                "failed_missions": 0,
                "critical_missions": 0}
    logger.info("showing summary")
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
    logger.info("attempt to get missions-by-status")
    if not adb.get_all_agents() or not mdb.get_all_missions():
        logger.info("no data")
        return {"open": 0,"in_progress": 0,"completed": 0,"failed": 0,"cancelled": 0}
    logger.info("showing missions-by-status")
    return {
            "open": mdb.count_open_missions(),
            "in_progress": mdb.count_by_status("IN_PROGRESS"),
            "completed": mdb.count_by_status("COMPLETED"),
            "failed": mdb.count_by_status("FAILED"),
            "critical": mdb.count_by_status("CRITICAL")
            }


@router.get("/reports/top-agent")
def top_agent():
    logger.info("attempt to get top agent")
    if not adb.get_all_agents():
        logger.info("no data")
        raise HTTPException(404, "No agents")
    logger.info("showing top agent")
    return mdb.get_top_agent()
