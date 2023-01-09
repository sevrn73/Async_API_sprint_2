import pytest


@pytest.mark.asyncio
async def test_get_search(make_get_request):
    """Тест поиска записи по фразе"""

    # получаем все фильмы из elasticsearch
    film =   {
        "id": "92dcddff-a70e-497c-92dc-0da12d1d528a",
        "title": "Exile: A Star Wars Story",
        "imdb_rating": 5.8
    }
    response = await make_get_request('/films/search/', {'query': 'Exile'})
    assert response.status == 200

    assert response.body[0] == film


@pytest.mark.asyncio
async def test_get_n(make_get_request):
    """Тест проверяет вывод N записей"""

    response = await make_get_request('/films/search/', {'query':'war', 'page[number]': 1, 'page[size]': 3})

    # Проверка результата
    assert response.status == 200

    assert len(response.body) == 3


@pytest.mark.asyncio
async def test_validator_1(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/films/search/123')
    assert response.status == 404

@pytest.mark.asyncio
async def test_validator_2(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/films/search/}', {'query':3131})
    assert response.status == 404

@pytest.mark.asyncio
async def test_validator_3(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/films/search/', {'page[number]': 0})
    assert response.status == 422

@pytest.mark.asyncio
async def test_validator_4(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/films/search/', {'page[size]': 0})
    assert response.status == 422

@pytest.mark.asyncio
async def test_redis(make_get_request):
    """Тест кэширования"""
    # этот запрос сделан без удаления кэша
    response = await make_get_request('/films/search/', {'query':'war', 'page[number]': 1, 'page[size]': 10}, False)
    assert response.status == 200

    response2 = await make_get_request('/films/search/', {'query':'war', 'page[number]': 1, 'page[size]': 10})
    assert response.status == 200

    assert response.resp_speed > response2.resp_speed
