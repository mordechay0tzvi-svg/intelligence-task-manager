from database.db_connection import DBconnection
c = DBconnection()

class AgentsDB:
    def __init__(self):
        pass

    def create_agent(self, data:dict):
        conn = c.get_connector()
        cursor = conn.cursor()
        sql = """insert into agents(name, scecialty, completed_missions, failed_missions, agent_rank) values(%s,%s,%s,%s,%s)"""
        values = (data['name'], data['specialty'], data['completed_missions'], data['failed_missions'], data['agent_rank'])
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        #return ?
    
    def get_all_agents(self):
        conn = c.get_connector()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""select * from agents""")
        conn.commit()
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    
    
