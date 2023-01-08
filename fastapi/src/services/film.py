from functools import lru_cache
from typing import Optional, List
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from services.base_service import BaseService
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import ESFilm
from storage.film import FilmStorage
from cache.redis_cache import RedisCache


class FilmService(BaseService):
    def __init__(self, redis_cache: RedisCache, storage: FilmStorage):
        super().__init__(redis_cache, storage)

    async def get_page_number(
        self, es_index: str, rating_filter: float, sort: bool, page_number: int, page_size: int
    ) -> Optional[List[ESFilm]]:
        data = await self.redis_cache._many_data_from_cache(
            f"{es_index}::rating_filter::{rating_filter}::sort::{sort}::page_number::{page_number}::page_size::{page_size}"
        )
        if not data:
            data = await self.storage._get_data_from_elastic(es_index, rating_filter, sort, page_number, page_size)
            if not data:
                return None
            await self.redis_cache._put_many_data_to_cache(
                f"{es_index}::rating_filter::{rating_filter}::sort::{sort}::page_number::{page_number}::page_size::{page_size}",
                data,
            )
        return data

    async def get_by_list_id(self, es_index: str, film_ids: List[str]) -> Optional[List[ESFilm]]:
        data = await self.redis_cache._many_data_from_cache(f"{es_index}::film_ids{film_ids}")
        if not data:
            data = await self.storage._get_data_from_elastic_with_list_id(es_index, film_ids)
            if not data:
                return None
            await self.redis_cache._put_many_data_to_cache(
                f"{es_index}::film_ids{film_ids}",
                data,
            )
        return data

    async def get_request(
        self, es_index: str, query: str, sort: bool, page_number: int, page_size: int
    ) -> Optional[List[ESFilm]]:
        data = await self.redis_cache._many_data_from_cache(
            f"{es_index}::query::{query}::sort::{sort}::page_number::{page_number}::page_size::{page_size}"
        )
        if not data:
            data = await self.storage._get_request(es_index, query, sort, page_number, page_size)
            if not data:
                return None
            await self.redis_cache._put_many_data_to_cache(
                f"{es_index}::query::{query}::sort::{sort}::page_number::{page_number}::page_size::{page_size}",
                data,
            )
        return data


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    redis_cache = RedisCache(redis, ESFilm)
    storage = FilmStorage(elastic, ESFilm)
    return FilmService(redis_cache, storage)
