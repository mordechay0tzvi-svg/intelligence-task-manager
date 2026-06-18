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
    data = data.model_dump()
    if not data:
        raise HTTPException(422, "empty body") 
    for f in ["title", "description", "location", "difficulty", "importance"]:
        if f not in data.keys():
            raise HTTPException(422, f"{f} is missing")
    if data["importance"] not in mdb.range:
        raise HTTPException(400, "importance level must be between 1-10")
    if data["difficulty"] not in mdb.range:
        raise HTTPException(400, "difficulty level must be between 1-10")
    new_id = mdb.create_mission(data)
    mission = mdb.get_mission_by_id(new_id)
    return {"message":("mission created", mission)}


@router.get("/missions")
def all_missions():
    return mdb.get_all_missions()

@router.get("/missions/{id}")
def get_missions(id:int):
    mission = mdb.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, "mission not found")
    return mission

@router.put("/missions/{id}/assign/{agent_id}")
def assign_mission(id:int, agent_id:int):
    mission = mdb.get_mission_by_id(id)
    agent = adb.get_agent_by_id(agent_id)
    if not mission:
        raise HTTPException(404, "mission not found")
    if not agent:
        raise HTTPException(404, "agent not found")
    if not agent['is_active']:
        raise HTTPException(400, "Only active agent can be assigned")
    if mission['status'] != 'NEW':
        raise HTTPException(400, "Only new mission can be assigned")
    if len(mdb.get_open_missions_by_agent(agent_id)) >= 3:
        raise HTTPException(400, "Agent cannot be assigned more then 3 missions")
    if agent["agent_rank"] in ['Senior', 'Junior'] and mission['risk_level'] == 'CRITICAL':
        raise HTTPException(400, "Only a commander can be assigned a critical mission")
    mdb.assign_mission(id, agent_id)
    return {"message":"mission assigned successfully"}

    

@router.get("/mission/{id}/start")
def start_mission(id:int):
    mission = mdb.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, "mission not found")
    if mission["status"] != 'ASSIGNED':
        raise HTTPException(400, "only assigned mission can be started")
    mdb.update_mission_status(id, "IN_PROGRESS")
    return {"message": "mission started"}

@router.put("/missions/{id}/complete")
def complete_mission(id:int):
    mission = mdb.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, "mission not found")
    agent_id = mission["assingned_agent_id"]
    if mission["status"] != "IN_PROGRESS":
        raise HTTPException(400, "Only in progress mission can be completed")
    mdb.update_mission_status(id, 'COMPLETED')
    adb.increment_completed(agent_id)
    return {"message":"mission completed successfully"}

@router.put("/missions/{id}/fail")
def fail_mission(id:int):
    mission = mdb.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, "mission not found")
    agent_id = mission["assingned_agent_id"]
    if mission["status"] != "IN_PROGRESS":
        raise HTTPException(400, "Only in progress mission can be failed")
    mdb.update_mission_status(id, 'FAILED')
    adb.increment_failed(agent_id)
    return {"message":"mission failed successfully"}

@router.put("/missions/{id}/cancel")
def cancel_mission(id:int):
    mission = mdb.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, "mission not found")
    agent_id = mission["assingned_agent_id"]
    if mission["status"] not in ["NEW", "ASSIGNED"]:
        raise HTTPException(400, "Mission cannot be cancelled")
    mdb.update_mission_status(id, 'CANCELLED')
    adb.increment_failed(agent_id)
    return {"message":"mission cancelled successfully"}



