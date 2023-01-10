from functools import lru_cache
from typing import Optional
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from services.base_service import BaseService
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import ESGenre
from storage.base import BaseElasticStorage
from cache.redis_cache import RedisCache


class GenreService(BaseService):
    def __init__(self, redis_cache: RedisCache, storage: BaseElasticStorage):
        super().__init__(redis_cache, storage)


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    redis_cache = RedisCache(redis, ESGenre)
    storage = BaseElasticStorage(elastic, ESGenre)
    return GenreService(redis_cache, storage)
