import abc
from aioredis import Redis
from models.base_model import BaseModel


class BaseCache:
    def __init__(self, redis: Redis, model: BaseModel) -> None:
        self.redis = redis
        self.model = model

    @abc.abstractmethod
    async def _data_from_cache(self, redis_key: str):
        pass

    @abc.abstractmethod
    async def _put_data_to_cache(self, redis_key: str, data) -> None:
        pass

    @abc.abstractmethod
    async def _many_data_from_cache(self, redis_key: str):
        pass

    @abc.abstractmethod
    async def _put_many_data_to_cache(self, redis_key: str, data) -> None:
        pass
