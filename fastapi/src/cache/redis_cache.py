import json
from typing import Optional, List
from pydantic import parse_raw_as
from pydantic.json import pydantic_encoder
from aioredis import Redis
from models.base_model import BaseModel
from cache.base import BaseCache
from core.config import ProjectSettings


class RedisCache(BaseCache):
    def __init__(self, redis: Redis, model: BaseModel) -> None:
        super().__init__(redis, model)

    async def _data_from_cache(self, redis_key: str) -> Optional[BaseModel]:
        data = await self.redis.get(redis_key)
        if not data:
            return None
        data = self.model.parse_raw(data)
        return data

    async def _put_data_to_cache(self, redis_key: str, data: BaseModel) -> None:
        await self.redis.set(redis_key, data.json(), expire=ProjectSettings().CACHE_EXPIRE_IN_SECONDS)

    async def _many_data_from_cache(self, redis_key: str) -> Optional[List[BaseModel]]:
        data = await self.redis.get(redis_key)
        if not data:
            return None
        data = parse_raw_as(List[self.model], data)
        return data

    async def _put_many_data_to_cache(self, redis_key: str, data: List[BaseModel]) -> None:
        await self.redis.set(
            redis_key, json.dumps(data, default=pydantic_encoder), expire=ProjectSettings().CACHE_EXPIRE_IN_SECONDS
        )
