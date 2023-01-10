from typing import Optional
from fastapi import Query

from models.base_model import BaseModel
from storage.base import BaseElasticStorage
from cache.base import BaseCache


class BaseService:
    def __init__(self, redis_cache: BaseCache, storage: BaseElasticStorage):
        self.redis_cache = redis_cache
        self.storage = storage

    async def get_by_id(self, es_index: str, data_id: str) -> Optional[BaseModel]:
        data = await self.redis_cache._data_from_cache(f'{es_index}::data_id::{data_id}')
        if not data:
            data = await self.storage._get(es_index, data_id)
            if not data:
                return None
            await self.redis_cache._put_data_to_cache(f'{es_index}::data_id::{data_id}', data)
        return data

    async def get_page_number(
        self, es_index: str, sort: bool, page_number: int, page_size: int
    ) -> Optional[BaseModel]:
        data = await self.redis_cache._many_data_from_cache(
            f'{es_index}::sort::{sort}::page_number::{page_number}::page_size::{page_size}'
        )
        if not data:
            data = await self.storage._get_data(es_index, sort, page_number, page_size)
            if not data:
                return None
            await self.redis_cache._put_many_data_to_cache(
                f'{es_index}::sort::{sort}::page_number::{page_number}::page_size::{page_size}',
                data,
            )
        return data
