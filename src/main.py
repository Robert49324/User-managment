import logging
import logging.config
import uvicorn
from fastapi import FastAPI

logging.config.fileConfig('../logging.ini')
logger = logging.getLogger('user_managment')

app = FastAPI()

@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": "check"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
