from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('movie', env='ES_INDEX')
    # es_user: str = ...
    # es_password: str = ...
    es_index: str = Field('movie', env='ES_INDEX')
    es_id_field: str = Field('0', env='ES_ID_FIELD')
    # es_index_mapping: dict = ...

    redis_host: str = Field('redis', env='REDIS_HOST')
    redis_port: str = Field('6379', env='REDIS_PORT')

    service_url: str = Field('http://0.0.0.0:8001', env='FASTAPI_HOST')


TEST_SETTINGS = TestSettings()