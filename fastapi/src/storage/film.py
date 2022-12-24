from typing import Optional, List
from elasticsearch import AsyncElasticsearch, NotFoundError
from storage.base import BaseStorage
from models.film import ESFilm


class FilmStorage(BaseStorage):
    def __init__(self, elastic: AsyncElasticsearch) -> None:
        super().__init__(elastic)

    async def _get_data_from_elastic(
        self, es_index: str, rating_filter: float, sort: bool, page_number: int, data_on_page: int
    ) -> Optional[List[ESFilm]]:
        try:
            data = await self.elastic.search(
                index=es_index,
                from_=page_number,
                body={
                    "query": {
                        "range": {
                            "imdb_rating": {
                                "gte": rating_filter if rating_filter else 0,
                            }
                        }
                    }
                },
                size=data_on_page,
                sort=f"imdb_rating:{'asc' if sort else 'desc'}",
            )
        except NotFoundError:
            return None
        return [self.model(**_["_source"]) for _ in data["hits"]["hits"]]
