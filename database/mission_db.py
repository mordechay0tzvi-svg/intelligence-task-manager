from db_connection import c

class MissionsDB:
    def __init__(self):
        pass
    
    def create_mission(self,data:dict):
        difficulty = data["difficulty"]
        importance = data["importance"]
        risklevel = difficulty * 2 + importance
        conn = c.get_connector()
        cursor = conn.cursor()
        sql = """insert into missions(title, description, location, difficulty, importance, status, risk_level, assingned_agent_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (data['title'], data['description'], data['location'], difficulty, importance, 'NEW', risklevel, data["assigned_agent_id"])
        cursor.execute(sql, values)
        new_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        new_mission = data
        new_mission["id"] = new_id
        new_mission['status'] = 'NEW'
        new_mission['risk_level'] = risklevel
        return new_mission
    
    def get_all_missions(self):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from missions")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            return []
        return rows
    
    def get_mission_by_id(self, id:int):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from missions where id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        return row

    def assign_mission(self, m_id:int, a_id:int):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("update missions set assingned_agent_id = %s where id = %s", (a_id, m_id))
        assigend = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return assigend
    
    def update_mission_status(self, id:int, status:str):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("update missions set status = %s where id = %s", (status ,id))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return updated
            
m = MissionsDB()
m.update_mission_status(1, 'CANCELLED')






