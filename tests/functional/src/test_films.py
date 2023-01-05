import pytest


@pytest.mark.asyncio
async def test_get_all_films(make_get_request, get_all_data_elastic):
    """Тест запроса для всех фильмов"""

    # получаем все фильмы из elasticsearch
    all_films = await get_all_data_elastic('movies')

    response = await make_get_request('/films/movies/', {'page[number]': 1, 'page[size]': 1000})
    assert response.status == 200

    assert len(response.body) + 1 == len(all_films)


@pytest.mark.asyncio
async def test_get_by_id(make_get_request):
    """Тест проверяет работу получения по id в эндпоинте film"""

    response = await make_get_request('/films/c06dd0f4-d75d-4952-a81c-36837a30351b')
    film_data = {
        "id": "c06dd0f4-d75d-4952-a81c-36837a30351b",
        "title": "Frat Star",
        "imdb_rating": 3.5
    }
    # Проверка результата
    assert response.status == 200

    assert response.body == film_data


@pytest.mark.asyncio
async def test_validator_1(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/films')
    assert response.status == 404

@pytest.mark.asyncio
async def test_validator_2(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/films/wrong-uuid')
    assert response.status == 404

@pytest.mark.asyncio
async def test_validator_3(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/films/movies/', {'page[number]': 0})
    assert response.status == 422

@pytest.mark.asyncio
async def test_validator_4(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/films/movies/', {'page[size]': 0})
    assert response.status == 422

@pytest.mark.asyncio
async def test_redis(make_get_request):
    """Тест кэширования"""
    # этот запрос сделан без удаления кэша
    response = await make_get_request('/films/movies/', {'page[number]': 1, 'page[size]': 10}, False)
    assert response.status == 200

    response2 = await make_get_request('/films/movies/', {'page[number]': 1, 'page[size]': 10})
    assert response.status == 200

    assert response.resp_speed > response2.resp_speed