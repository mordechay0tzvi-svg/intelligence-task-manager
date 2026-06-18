from database.agent_db import adb

from fastapi import Body, Query, APIRouter, HTTPException

router = APIRouter()

@router.post("/agents")
def add_agent(data:dict =Body(...)):
    pass

@router.get("/agents")
def all_agents():
    pass

@router.get("/agents/{id}")
def get_angent(id:int):
    pass

@router.put("/agents/{id}")
def update_agent(id:int, data:dict=Body(...)):
    pass

@router.put("/agents/{id}")
def deactivate_agent(id:int):
    pass

@router.get("/agents/{id}/performance")
def get_performance(id:int):
    pass

