import json
from typing import Optional, List
from pydantic import parse_raw_as
from pydantic.json import pydantic_encoder
from aioredis import Redis
from fastapi import Query

from core.config import ProjectSettings
from models.base_model import BaseModel
from storage.base import BaseStorage


class BaseService:
    def __init__(self, redis: Redis, storage: BaseStorage):
        self.redis = redis
        self.storage = storage
        self.model = BaseModel

    async def get_by_id(self, es_index: str, data_id: str) -> Optional[BaseModel]:
        data = await self._data_from_cache(f"{es_index}::data_id::{data_id}")
        if not data:
            data = await self.storage._get_from_elastic(es_index, data_id)
            if not data:
                return None
            await self._put_data_to_cache(f"{es_index}::data_id::{data_id}", data)
        return data

    async def _data_from_cache(self, redis_key: str) -> Optional[BaseModel]:
        data = await self.redis.get(redis_key)
        if not data:
            return None
        data = self.model.parse_raw(data)
        return data

    async def _put_data_to_cache(self, redis_key: str, data: BaseModel) -> None:
        await self.redis.set(redis_key, data.json(), expire=ProjectSettings().CACHE_EXPIRE_IN_SECONDS)

    async def get_page_number(self, es_index: str, sort: bool, page_number: int, page_size: int) -> Optional[BaseModel]:
        data = await self._many_data_from_cache(
            f"{es_index}::sort::{sort}::page_number::{page_number}::page_size::{page_size}"
        )
        if not data:
            data = await self.storage._get_data_from_elastic(es_index, sort, page_number, page_size)
            if not data:
                return None
            await self._put_many_data_to_cache(
                f"{es_index}::sort::{sort}::page_number::{page_number}::page_size::{page_size}",
                data,
            )
        return data

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
