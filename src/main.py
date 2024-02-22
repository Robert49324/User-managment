import uvicorn
from fastapi import FastAPI

from auth.router import auth
from config import settings
from logger import logger
from user.router import user

app = FastAPI()

app.include_router(auth)
app.include_router(user)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    logger.info(f"Server started on {settings.host}:{settings.port}")
    uvicorn.run(app, host=settings.host, port=settings.port)
