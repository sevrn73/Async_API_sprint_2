import pytest


@pytest.mark.asyncio
async def test_get_all_persons(make_get_request, get_all_data_elastic):
    """Тест запроса для всех персон"""
    all_persons = await get_all_data_elastic('persons')

    response = await make_get_request('/persons/persons/', {'page[size]': 5000, 'page[number]': 1})

    assert response.status == 200

    assert len(response.body) + 1 == len(all_persons)

@pytest.mark.asyncio
async def test_get_by_id(make_get_request):
    """Тест проверяет работу получения по id в эндпоинте persons"""

    response = await make_get_request('/persons/e039eedf-4daf-452a-bf92-a0085c68e156')
    person_data = {
        "id": "e039eedf-4daf-452a-bf92-a0085c68e156",
        "name": "Peter Cushing"
        }
    # Проверка результата
    assert response.status == 200

    assert response.body == person_data

@pytest.mark.asyncio
async def test_get_films_by_peson_id( prepare_es_film, make_get_request):
    """Тест проверяет получение фильмов по uuid персоны"""
    film = prepare_es_film[0]
    short_film = {'id': film.get('id'),
                  'title': film.get('title'),
                  'imdb_rating': film.get('imdb_rating')}

    response = await make_get_request('/person/7f489c61-1a21-43d2-a3ad-3d900f8a9b5e/films')

    assert response.status == 200

    assert response.body[0] == short_film

@pytest.mark.asyncio
async def test_validator_1(make_get_request):
    """Тест корректной валидации форм"""

    response = await make_get_request('/persons/')
    assert response.status == 404

@pytest.mark.asyncio
async def test_validator_2(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/persons/wrong-uuid')
    assert response.status == 404

@pytest.mark.asyncio
async def test_validator_3(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/persons/persons/', {'page[number]': 0})
    assert response.status == 422

@pytest.mark.asyncio
async def test_validator_4(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/persons/persons/', {'page[size]': 0})
    assert response.status == 422

@pytest.mark.asyncio
async def test_redis(make_get_request):
    """Тест кэширования"""
    # этот запрос сделан без удаления кэша
    response = await make_get_request('/persons/persons/', {'page[number]': 1, 'page[size]': 100}, False)
    assert response.status == 200

    # в этом запросе мы получаем результат кэша от первого запроса
    # и сравниваем затраченное время
    response2 = await make_get_request('/persons/persons/', {'page[number]': 1, 'page[size]': 100})
    assert response.status == 200

    assert response.resp_speed > response2.resp_speed
