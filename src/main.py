import uvicorn
from fastapi import FastAPI

from auth.router import auth
from logger import logger

app = FastAPI()

app.include_router(auth)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    logger.info("Server started")
    uvicorn.run(app, host="0.0.0.0", port=8000)
