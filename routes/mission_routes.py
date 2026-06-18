from database.mission_db import mdb
from database.agent_db import adb
from logs.logger import logger
from fastapi import Body, Query, APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Mission(BaseModel):
    title:str
    description:str
    location:str
    difficulty:int
    importance:int


@router.post("/missions")
def add_mission(data:Mission =Body(...)):
    logger.info("add mission attempt")
    data = data.model_dump()
    if not data:
        logger.error("empty body")
        raise HTTPException(422, "empty body") 
    for f in ["title", "description", "location", "difficulty", "importance"]:
        if f not in data.keys():
            logger.error("key missing")
            raise HTTPException(422, f"{f} is missing")
    if data["importance"] not in mdb.range:
        logger.error("importance is not 1-10")
        raise HTTPException(400, "importance level must be between 1-10")
    if data["difficulty"] not in mdb.range:
        logger.error("difficulty is not 1-10")
        raise HTTPException(400, "difficulty level must be between 1-10")
    new_id = mdb.create_mission(data)
    mission = mdb.get_mission_by_id(new_id)
    logger.info("mission added")
    return {"message":("mission created", mission)}


@router.get("/missions")
def all_missions():
    logger.info("getting all missions")
    return mdb.get_all_missions()

@router.get("/missions/{id}")
def get_missions(id:int):
    logger.info("get mission attempt")
    mission = mdb.get_mission_by_id(id)
    if not mission:
        logger.error("mission not found")
        raise HTTPException(404, "mission not found")
    logger.info("mission found")
    return mission

@router.put("/missions/{id}/assign/{agent_id}")
def assign_mission(id:int, agent_id:int):
    logger.info("mission assignment attempt")
    mission = mdb.get_mission_by_id(id)
    agent = adb.get_agent_by_id(agent_id)
    if not mission:
        logger.error("mission not found")
        raise HTTPException(404, "mission not found")
    if not agent:
        logger.error("agent not found")
        raise HTTPException(404, "agent not found")
    if not agent['is_active']:
        logger.error("agent not active")
        raise HTTPException(400, "Only active agent can be assigned")
    if mission['status'] != 'NEW':
        logger.error("mission is not assignable")
        raise HTTPException(400, "Only new mission can be assigned")
    if len(mdb.get_open_missions_by_agent(agent_id)) >= 3:
        logger.error("agent has 3 missions in progress")
        raise HTTPException(400, "Agent cannot be assigned more then 3 missions")
    if agent["agent_rank"] in ['Senior', 'Junior'] and mission['risk_level'] == 'CRITICAL':
        logger.error("agent not ranked high for critical mission")
        raise HTTPException(400, "Only a commander can be assigned a critical mission")
    mdb.assign_mission(id, agent_id)
    logger.info("mission assigned")
    return {"message":"mission assigned successfully"}

    

@router.get("/mission/{id}/start")
def start_mission(id:int):
    logger.info("mission start attempt")
    mission = mdb.get_mission_by_id(id)
    if not mission:
        logger.error("mission not found")
        raise HTTPException(404, "mission not found")
    if mission["status"] != 'ASSIGNED':
        logger.error("mission cannot be assigned")
        raise HTTPException(400, "only assigned mission can be started")
    mdb.update_mission_status(id, "IN_PROGRESS")
    logger.info("mission started")
    return {"message": "mission started"}

@router.put("/missions/{id}/complete")
def complete_mission(id:int):
    logger.info("mission complete attempt")
    mission = mdb.get_mission_by_id(id)
    if not mission:
        logger.error("mission not found")
        raise HTTPException(404, "mission not found")
    agent_id = mission["assingned_agent_id"]
    if mission["status"] != "IN_PROGRESS":
        logger.error("mission not in progress")
        raise HTTPException(400, "Only in progress mission can be completed")
    mdb.update_mission_status(id, 'COMPLETED')
    adb.increment_completed(agent_id)
    logger.info("mission completed")
    return {"message":"mission completed successfully"}

@router.put("/missions/{id}/fail")
def fail_mission(id:int):
    logger.info("failing mission attempt")
    mission = mdb.get_mission_by_id(id)
    if not mission:
        logger.error("mission not found")
        raise HTTPException(404, "mission not found")
    agent_id = mission["assingned_agent_id"]
    if mission["status"] != "IN_PROGRESS":
        logger.error("mission not in progress")
        raise HTTPException(400, "Only in progress mission can be failed")
    mdb.update_mission_status(id, 'FAILED')
    adb.increment_failed(agent_id)
    logger.info("mission failed")
    return {"message":"mission failed successfully"}

@router.put("/missions/{id}/cancel")
def cancel_mission(id:int):
    logger.info("mission cancellation attempt")
    mission = mdb.get_mission_by_id(id)
    if not mission:
        logger.error("mission not found")
        raise HTTPException(404, "mission not found")
    agent_id = mission["assingned_agent_id"]
    if mission["status"] not in ["NEW", "ASSIGNED"]:
        logger.error("mission cannot be cancelled")
        raise HTTPException(400, "Mission cannot be cancelled")
    mdb.update_mission_status(id, 'CANCELLED')
    adb.increment_failed(agent_id)
    logger.info("mission cancelled")
    return {"message":"mission cancelled successfully"}



