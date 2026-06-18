from database.agent_db import adb

from fastapi import Body, Query, APIRouter, HTTPException

from pydantic import BaseModel

class Agent(BaseModel):
    name:str
    agent_rank:str
    specialty:str

router = APIRouter()

@router.post("/agents")
def add_agent(data:Agent =Body(...)):
    data = data.model_dump()
    if not data:
        raise HTTPException(422, "empty body") 
    for f in ['name', 'specialty','agent_rank']:
        if f not in data.keys():
            raise HTTPException(422, f"{f} is missing")
    if data["agent_rank"] not in adb.valid_ranks:
        raise HTTPException(400, "Invalid rank")
    new_id = adb.create_agent(data)
    return {201: ("agent created",adb.get_agent_by_id(new_id))}

@router.get("/agents")
def all_agents():
    return adb.get_all_agents()
    

@router.get("/agents/{id}")
def get_angent(id:int):
    agent = adb.get_agent_by_id(id)
    if agent == None:
        raise HTTPException(404, "agent not found")
    return agent

@router.put("/agents/{id}")
def update_agent(id:int, data:Agent=Body(...)):
    agent = adb.get_agent_by_id(id)
    if agent == None:
        raise HTTPException(404, "agent not found")
    data = data.model_dump()
    adb.update_agent(id, data)
    return {"message":"updated"}

@router.put("/agents/{id}/deactivate")
def deactivate_agent(id:int):
    agent = adb.get_agent_by_id(id)
    if agent == None:
        raise HTTPException(404, "agent not found")
    adb.deactivate_agent(id)
    return {"message":"agent deactivated"}


@router.get("/agents/{id}/performance")
def get_performance(id:int):
    agent = adb.get_agent_by_id(id)
    if agent == None:
        raise HTTPException(404, "agent not found")
    return adb.get_agent_performance(id)



