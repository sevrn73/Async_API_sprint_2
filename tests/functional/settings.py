from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://elasticsearch:9200', env='ES_HOST')
    es_index: str = Field('movies', env='ES_ID')
    es_id_field: str = Field('id', env='ES_ID_FIELD')


    redis_host: str = Field('redis', env='REDIS_HOST')
    redis_port: str = Field('6379', env='REDIS_PORT')

    service_url: str = Field('http://fastapi:8001', env='FASTAPI_HOST')



TEST_SETTINGS = TestSettings()