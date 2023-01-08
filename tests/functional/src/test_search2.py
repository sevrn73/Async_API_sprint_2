
import datetime
import uuid
import json

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

# from pydantic import BaseSettings, Field


# class TestSettings(BaseSettings):
#     es_host: str = Field('http://elasticsearch:9200', env='ES_HOST')
#     es_index: str = Field('movies', env='ES_ID')
#     es_id_field: str = Field('id', env='ES_ID_FIELD')


#     redis_host: str = Field('redis', env='REDIS_HOST')
#     redis_port: str = Field('6379', env='REDIS_PORT')

#     service_url: str = Field('http://fastapi:8001', env='FASTAPI_HOST')



# TEST_SETTINGS = TestSettings()
#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.

@pytest.mark.asyncio
async def test_search():

    # 1. Генерируем данные для ES

    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'film_work_type': 'movie'
    } for _ in range(60)]

    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': 'movies', '_id': row['id']}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    es_client = AsyncElasticsearch(hosts='http://elasticsearch:9200',
                                   validate_cert=False,
                                   use_ssl=False)
    response = await es_client.bulk(str_query, refresh=True)
    await es_client.close()
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')

    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = 'http://fastapi:8001' + '/api/v1/films/search'
    query_data = {'search': 'The Star'}
    async with session.get(url, params=query_data) as response:
        print(response)
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ

    assert status == 200
    assert len(response.body) == 50