from typing import List, Tuple
from elasticsearch import Elasticsearch, helpers
from pydantic import BaseModel
from backoff import backoff


class ESLoad:
    def __init__(self, es_host: str, es_user: str, es_password: str, model_name: str):
        self.es = Elasticsearch(es_host, basic_auth=(es_user, es_password), verify_certs=False)
        self.model_name = model_name

    @backoff()
    def send_data(self, es_data: List[BaseModel]) -> Tuple[int, list]:
        query = [{"_index": self.model_name, "_id": data.id, "_source": data.dict()} for data in es_data]
        helpers.bulk(self.es, query)
