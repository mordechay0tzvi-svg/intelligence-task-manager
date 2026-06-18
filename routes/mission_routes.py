from database.mission_db import mdb

from fastapi import Body, Query, APIRouter, HTTPException

router = APIRouter()

@router.post("/missions")
def add_mission(data:dict =Body(...)):
    pass

@router.get("/missions")
def all_missions():
    pass

@router.get("/missions/{id}")
def get_missions(id:int):
    pass

@router.put("/missions/{id}/assign/{agent_id}")
def assign_mission(id:int, agent_id:int):
    pass

@router.get("/mission/{id}/start")
def start_mission(id:int):
    pass

@router.put("/missions/{id}/complete")
def complete_nission(id:int):
    pass

@router.put("/missions/{id}/fail")
def fail_nission(id:int):
    pass

@router.put("/missions/{id}/cancel")
def cancel_nission(id:int):
    pass

