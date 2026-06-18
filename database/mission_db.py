from database.db_connection import c

def dicide_risklevel(num:int):
    if 0 <= num <= 9:
        return 'LOW'
    elif 10 <= num <= 17:
        return 'MEDIUM'
    elif 18 <= num <= 24:
        return 'HIGH'
    elif num >= 25:
        return 'CRITICAL'

class MissionsDB:
    def __init__(self):
        pass

    def create_mission(self,data:dict):
        difficulty = data["difficulty"]
        importance = data["importance"]
        risklevel_number = difficulty * 2 + importance
        risklevel = dicide_risklevel(risklevel_number)
        conn = c.get_connector()
        cursor = conn.cursor()
        sql = """insert into missions(title, description, location, difficulty, importance, status, risk_level, assingned_agent_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (data['title'], data['description'], data['location'], difficulty, importance, 'NEW', risklevel, None)
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
        cursor.execute("update missions set assingned_agent_id = %s, status = 'ASSIGNED' where id = %s", (a_id, m_id))
        assigend = cursor.rowcount > 0
        conn.commit()
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
            
    def get_open_missions_by_agent(self, id:int):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from missions where assingned_agent_id = %s and status in ('ASSIGNED', 'IN_PROGRESS')", (id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            return []
        return rows
    
    def count_all_missions(self):
        conn = c.get_connector()
        cursor = conn.cursor()
        cursor.execute("select count(*) from missions")
        rows = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return rows
    
    def count_by_status(swlf, status:str):
        conn = c.get_connector()
        cursor = conn.cursor()
        cursor.execute("select count(*) from missions where status = %s", (status,))
        rows = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return rows

    def count_open_missions(self):
        conn = c.get_connector()
        cursor = conn.cursor()
        cursor.execute("select count(*) from missions where status = 'NEW' or status = 'IN_PROGRESS' or status = 'ASSIGNED'")
        rows = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return rows
    
    def count_critical_missions(self):
        conn = c.get_connector()
        cursor = conn.cursor()
        cursor.execute("select count(*) from missions where risk_level = 'CRITICAL'")
        rows = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return rows
    
    def get_top_agent(self):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT assingned_agent_id, count(status) as t FROM missions where status = 'COMPLETED' group by assingned_agent_id order by t desc limit 1")
        top_agent_id = cursor.fetchone()["assingned_agent_id"]
        cursor.execute("select * from agents where id = %s",(top_agent_id, ))
        top = cursor.fetchone()
        cursor.close()
        conn.close()
        return top


mdb = MissionsDB()





