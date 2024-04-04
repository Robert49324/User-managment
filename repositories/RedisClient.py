import redis

from configs.environment import get_settings

settings = get_settings()


class RedisClient:
    def __init__(self):
        self.redis = redis.from_url(settings.redis_url)

    async def create(self, key, value):
        self.redis.set(key, value)

    async def read(self, key):
        return self.redis.get(key)

    async def update(self, key, value):
        if await self.redis.exists(key):
            await self.redis.set(key, value)

    async def delete(self, key):
        await self.redis.delete(key)
