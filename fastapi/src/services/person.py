from functools import lru_cache
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from services.base_service import BaseService
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import ESPerson
from storage.base import BaseElasticStorage
from cache.redis_cache import RedisCache


class PersonService(BaseService):
    def __init__(self, redis_cache: Redis, storage: BaseElasticStorage):
        super().__init__(redis_cache, storage)


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    redis_cache = RedisCache(redis, ESPerson)
    storage = BaseElasticStorage(elastic, ESPerson)
    return PersonService(redis_cache, storage)
