import mysql.connector
class DBconnection:
    def __init__(self):
        self.port=3306
        self.host="localhost"
        self.user='root'
        self.database='Intelligence_db'
        self.password='1234'

    def get_connector(self):
        return mysql.connector.connect(
                                       port=self.port,
                                       host=self.host,
                                       user=self.user,
                                       database=self.database,
                                       password=self.password
                                       )
    def create_database(self):
        conn = self.get_connector()
        cursor = conn.cursor()
        cursor.execute("""CREATE DATABASE IF NOT EXISTS Intelligence_db""")
        conn.commit()
        cursor.close()
        conn.close()

    def create_tables(self):
        conn = self.get_connector()
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS agents(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(100) NOT NULL,
                       scecialty VARCHAR(50) NOT NULL,
                       is_active BOOLEAN DEFAULT TRUE,
                       completed_missions INT NOT NULL,
                       failed_missions INT NOT NULL,
                       agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS missions(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       title VARCHAR(50) NOT NULL,
                       description VARCHAR(500) NOT NULL,
                       location VARCHAR(100),
                       difficulty INT,
                       importance INT,
                       status VARCHAR(20) NOT NULL,
                       risk_level VARCHAR(20)  NOT NULL,
                       assinged_agent_id INT)""")
        conn.commit()
        cursor.close()
        conn.close()

c = DBconnection()
c.create_database()
c.create_tables()



    
