# intelligence-task-manager
This project manages agent and missions data tables using sql.
An agent consists:
                id / number that automatically increses with every new row
                name / str
                specialty / str
                is_active / (true/false)
                completed_missions / number of completed missions
                failed_missions / number of failed missions
                agent_rank / (Junior / Senior / Commander)

A mission consists:
                id / number that automatically increses with every new row
                title / str
                description / str
                location / str
                difficulty / 1-10
                importance / 1-10
                status / (NEW / ASSIGNED / IN_PROGRESS / COMPLETED / FAILED / CANCELLED)
                risk_level / difficulty * 2 + importance 
                assigned_agent_id / agent assigned

Each table is managed by a class (AgentDB, MissionDB) that contains all the methods for managing the tabless using the class (DBconnection) that connects the to the database and the tables.

DBconnection class:
get_connection() - connection to the database
create_database() - creates the database if not exists
create_tables() - creates the tables (agents and missions)

AgentdB class:
create_agent(data) -> adds a new agent to the table 
get_all_agents() -> gives a list of all the agents
get_agent_by_id(id)	-> gets an agent by an id
update_agent(id, data) -> updates an agent 
deactivate_agent(id) -> deactivates an agent by an id
increment_completed(id)	-> increments the agents completed missions
increment_failed(id) -> increments the agents failed missions
get_agent_performance(id) -> gets the completed, failed, total missions and the succsses rate of an agent
count_active_agents() -> gives the number of active agents

MissionDB class:
create_mission(data) -> adds a new mission to the table 
get_all_missions() -> gives a list of all the mission
get_mission_by_id(id) -> gets a mission by it's id
assign_mission(m_id, a_id) -> assaign a mission to an agent 
update_mission_status(id, status) -> updates a mission
get_open_missions_by_agent(id) -> gets mission that assigned or in progress by/to the agent with that id
count_all_missions() -> the number of all the missions
count_by_status(status)	-> counts all the missions with the status given
count_open_missions() -> counts open missions
count_critical_missions() -> counts all the critical missions
get_top_agent() -> the agent with most completed missions

Files structure:

    intelligence-task-manager/
    ├── database/
    │   ├── db_connection.py
    │   ├── agent_db.py
    │   └── mission_db.py
    ├── README.md
    ├── requirements.txt
    └── .gitignore

Rules: This rules must be kept by the objects that manages the data tables.

1. agent_rank of an agent must be a: Junior / Senior / Commander.
2. difficulty and importance of a miision must be in range 1-10.
3. risk_level of a mission gets calculated automatically and not by the user.
4. non active agent cannot be assigned with new messages.
5. agent cannot be assined a new mission if he has 3 open missions.
6. if risk_level of a mission is critical only a commander allowed to be assigned to that missions.
7. only missions with status NEW can be assigned.
8. only assined missions can change status to in_progress. 
9. only in_progress missions can be finished with failed or completed.
10. only assined and new missions can be cancelled.


How to run: Instructions.

run: docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0

then use the managers to work with the database and the tables inside.







       





