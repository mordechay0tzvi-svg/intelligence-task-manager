from fastapi import FastAPI

import uvicorn

app = FastAPI()
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_routes import router as report_router

app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(report_router)

if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=8000)

