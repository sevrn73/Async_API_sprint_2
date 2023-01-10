import abc
from typing import Optional, List
from models.base_model import BaseModel
from elasticsearch import AsyncElasticsearch, NotFoundError


class BaseStorage:
    @abc.abstractmethod
    async def _get(self, index: str, data_id: str):
        pass

    @abc.abstractmethod
    async def _get_data(self, index: str, sort: bool, page_number: int, data_on_page: int):
        pass


class BaseElasticStorage(BaseStorage):
    def __init__(self, elastic: AsyncElasticsearch, model: BaseModel) -> None:
        self.elastic = elastic
        self.model = model

    async def _get(self, index: str, data_id: str) -> Optional[BaseModel]:
        try:
            doc = await self.elastic.get(index, data_id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])

    async def _get_data(
        self, index: str, sort: bool, page_number: int, data_on_page: int
    ) -> Optional[List[BaseModel]]:
        try:
            data = await self.elastic.search(
                index=index,
                from_=page_number,
                size=data_on_page,
                sort=f"{'genre' if index == 'genres' else 'name'}.keyword:{'asc' if sort else 'desc'}",
            )
        except NotFoundError:
            return None
        return [self.model(**_['_source']) for _ in data['hits']['hits']]
