import logging
frmt = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=frmt, filename='app.log')
logger = logging.getLogger(__name__)


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
    logger.info("logger loading")
    uvicorn.run(app, host="localhost", port=8000)

