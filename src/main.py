import logging
import logging.config
import uvicorn
from fastapi import FastAPI

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('User_managment')

app = FastAPI()

@app.get("/")
async def root():
    logger.debug("debug message", extra={"x": "hello"})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    return {"message": "check"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
