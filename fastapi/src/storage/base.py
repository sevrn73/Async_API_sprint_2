import abc
from typing import Optional, List
from models.base_model import BaseModel
from elasticsearch import AsyncElasticsearch, NotFoundError


class BaseStorage:
    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.elastic = elastic

    @abc.abstractmethod
    async def _get_from_elastic(self, es_index: str, data_id: str) -> Optional[BaseModel]:
        try:
            doc = await self.elastic.get(es_index, data_id)
        except NotFoundError:
            return None
        return self.model(**doc["_source"])

    @abc.abstractmethod
    async def _get_data_from_elastic(
        self, es_index: str, sort: bool, page_number: int, data_on_page: int
    ) -> Optional[List[BaseModel]]:
        try:
            data = await self.elastic.search(
                index=es_index,
                from_=page_number,
                size=data_on_page,
                sort=f"{'genre' if es_index == 'genres' else 'name'}.keyword:{'asc' if sort else 'desc'}",
            )
        except NotFoundError:
            return None
        return [self.model(**_["_source"]) for _ in data["hits"]["hits"]]
