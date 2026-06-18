from database.agent_db import adb
from fastapi import Body, Query, APIRouter, HTTPException
from pydantic import BaseModel
from logs.logger import logger

class Agent(BaseModel):
    name:str
    agent_rank:str
    specialty:str

router = APIRouter()

@router.post("/agents")
def add_agent(data:Agent =Body(...)):
    logger.info("add agent attempt")
    data = data.model_dump()
    if not data:
        logger.error("empty body")
        raise HTTPException(422, "empty body") 
    for f in ['name', 'specialty','agent_rank']:
        if f not in data.keys():
            logger.error("missing key")
            raise HTTPException(422, f"{f} is missing")
    if data["agent_rank"] not in adb.valid_ranks:
        logger.error("invalid rank")
        raise HTTPException(400, "Invalid rank")
    new_id = adb.create_agent(data)
    logger.info("agent added")
    return {201: ("agent created",adb.get_agent_by_id(new_id))}

@router.get("/agents")
def all_agents():
    logger.info("showing all agents")
    return adb.get_all_agents()
    

@router.get("/agents/{id}")
def get_angent(id:int):
    logger.info("get agent by id attempt")
    agent = adb.get_agent_by_id(id)
    if agent == None:
        logger.info("agent not found")
        raise HTTPException(404, "agent not found")
    logger.info("agent found")
    return agent

@router.put("/agents/{id}")
def update_agent(id:int, data:Agent=Body(...)):
    logger.info("update agent attempt")
    agent = adb.get_agent_by_id(id)
    if agent == None:
        logger.error("agent not found")
        raise HTTPException(404, "agent not found")
    data = data.model_dump()
    adb.update_agent(id, data)
    logger.info("agent updated")
    return {"message":"updated"}

@router.put("/agents/{id}/deactivate")
def deactivate_agent(id:int):
    logger.info("agent deactivate attempt")
    agent = adb.get_agent_by_id(id)
    if agent == None:
        logger.error("agent not found")
        raise HTTPException(404, "agent not found")
    adb.deactivate_agent(id)
    logger.info("agent deactivated")
    return {"message":"agent deactivated"}


@router.get("/agents/{id}/performance")
def get_performance(id:int):
    logger.info("getting agent performance attempt")
    agent = adb.get_agent_by_id(id)
    if agent == None:
        logger.info("agent not foun")
        raise HTTPException(404, "agent not found")
    logger.info("agent performance shown")
    return adb.get_agent_performance(id)



