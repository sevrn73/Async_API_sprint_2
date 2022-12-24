
import datetime
import uuid
from typing import List

import aiohttp
import pytest

from tests.functional.settings import TEST_SETTINGS


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'search': 'The Star'},
                {'status': 200, 'length': 50}
        ),
        (
                {'search': 'Mashed potato'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search2(make_get_request, es_write_data, es_data: List[dict], query_data: dict, expected_answer: dict):
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

    await es_write_data(es_data)
    session = aiohttp.ClientSession()
    url = TEST_SETTINGS.service_url + '/api/v1/search'
    query_data = {'search': 'The Star'}
    response = await make_get_request('/search', query_data)
    body = await response.json()
    headers = response.headers
    status = response.status
    assert status == expected_answer["status"]
    assert len(response.body) == expected_answer["length"]