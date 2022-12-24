from functools import lru_cache
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from services.base_service import BaseService
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import ESPerson
from storage.base import BaseStorage


class PersonService(BaseService):
    def __init__(self, redis: Redis, storage: BaseStorage):
        super().__init__(redis, storage)
        self.model = ESPerson


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    storage = BaseStorage(elastic)
    return PersonService(redis, storage)
