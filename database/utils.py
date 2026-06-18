from agent_db import get_agent_by_id

def dicide_risklevel(num:int):
    if 0 <= num <= 9:
        return 'LOW'
    elif 10 <= num <= 17:
        return 'MEDIUM'
    elif 18 <= num <= 24:
        return 'HIGH'
    elif num >= 25:
        return 'CRITICAL'
    
def check_difficulty_or_importance(num:int):
    return 1 <= num <= 10

def rank_validater(agent_rank:str):
    return agent_rank in ['Senior', 'Junior', 'Commander']

def dynamic_agent_updading(data:dict, id:int):
    new_data = get_agent_by_id(id)
    for k, v in data.items():
        new_data[k] = v
    return new_data



 
