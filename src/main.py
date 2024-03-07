import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from auth.router import auth
from config import settings
from logger import logger
from user.router import user, users
from group.router import group

app = FastAPI()
add_pagination(app)

app.include_router(auth)
app.include_router(user)
app.include_router(users)
app.include_router(group)

@app.get("/healthcheck", include_in_schema=False, status_code=200)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    logger.info(f"Server started on {settings.host}:{settings.port}")
    uvicorn.run(app, host=settings.host, port=settings.port)
