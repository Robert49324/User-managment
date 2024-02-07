import logging
import logging.config
import sys

import uvicorn
from fastapi import FastAPI

from auth.router import auth

# logging.config.fileConfig("../logging.ini")
# logger = logging.getLogger("user_managment")

app = FastAPI()
app.include_router(auth)


@app.get("/")
async def root():
    # logger.debug("Root endpoint called")
    return {"message": "check"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
