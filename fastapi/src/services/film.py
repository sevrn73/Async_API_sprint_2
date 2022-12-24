from functools import lru_cache
from typing import Optional, List
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from services.base_service import BaseService
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import ESFilm
from storage.film import FilmElasticStorage


class FilmService(BaseService):
    def __init__(self, redis: Redis, storage: FilmElasticStorage):
        super().__init__(redis, storage)
        self.model = ESFilm

    async def get_page_number(
        self, es_index: str, rating_filter: float, sort: bool, page_number: int, page_size: int
    ) -> Optional[List[ESFilm]]:
        data = await self._many_data_from_cache(
            f"{es_index}::rating_filter::{rating_filter}::sort::{sort}::page_number::{page_number}::page_size::{page_size}"
        )
        if not data:
            data = await self.storage._get_data_from_elastic(es_index, rating_filter, sort, page_number, page_size)
            if not data:
                return None
            await self._put_many_data_to_cache(
                f"{es_index}::rating_filter::{rating_filter}::sort::{sort}::page_number::{page_number}::page_size::{page_size}",
                data,
            )
        return data


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    storage = FilmElasticStorage(elastic)
    return FilmService(redis, storage)
