from functools import lru_cache
from typing import Optional
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from services.base_service import BaseService
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import ESGenre
from storage.base import BaseStorage


class GenreService(BaseService):
    def __init__(self, redis: Redis, storage: BaseStorage):
        super().__init__(redis, storage)
        self.model = ESGenre


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    storage = BaseStorage(elastic)
    return GenreService(redis, storage)
