from database.db_connection import c

class AgentsDB:
    def __init__(self):
        pass

    valid_ranks = ["Junior", "Senior", "Commander"]

    def create_agent(self, data:dict):
        conn = c.get_connector()
        cursor = conn.cursor()
        sql = """insert into agents(name, specialty, agent_rank) values(%s,%s,%s)"""
        values = (data['name'], data['specialty'], data['agent_rank'])
        cursor.execute(sql, values)
        new_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return new_id
    
    def get_all_agents(self):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""select * from agents""")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            return []
        return rows
    
    def get_agent_by_id(self, id:int):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from agents where id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        return row
   
    def update_agent(self, id:int, data:dict): 
        agent = self.get_agent_by_id(id)
        for k, v in data.items():
            agent[k] = v 
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        sql = """update agents set name = %s, specialty = %s, is_active = %s, completed_missions = %s, failed_missions = %s, agent_rank = %s where id = %s"""
        values = (agent['name'], agent['specialty'], agent['is_active'], agent['completed_missions'], agent['failed_missions'], agent['agent_rank'], id)
        cursor.execute(sql, values)
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return updated

    def deactivate_agent(self, id:int):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("update agents set is_active = False where id = %s", (id,))
        conn.commit()
        deactivated = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return deactivated
    
    def increment_completed(self, id:int):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("update agents set completed_missions = completed_missions + 1 where id = %s", (id,))
        conn.commit()
        incremented = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return incremented

    def increment_failed(self, id:int):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("update agents set failed_missions = failed_missions + 1 where id = %s", (id,))
        conn.commit()
        incremented = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return incremented

    def get_agent_performance(self, id:int):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select completed_missions, failed_missions from agents where id = %s", (id,))
        data  = cursor.fetchone()
        performance = {}
        performance["completed"], performance["failed"] = data["completed_missions"], data["failed_missions"]
        performance["total"] = performance["completed"] + performance["failed"]
        if performance["total"] == 0:
            return {"message":"no missions yet"}
        performance['success_rate'] = (performance["completed"] / performance["total"]) * 100 
        cursor.close()
        conn.close()
        return performance
    
    def count_active_agents(self):
        conn = c.get_connector()
        cursor = conn.cursor()
        cursor.execute("select count(*) from agents where is_active")
        active  = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return active

adb = AgentsDB()   
