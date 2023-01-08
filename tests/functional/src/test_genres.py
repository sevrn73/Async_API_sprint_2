import pytest


@pytest.mark.asyncio
async def test_genres_all_valid_data(make_get_request):
    """Тест запроса для всех жанров"""
    # Выполнение запроса
    response = await make_get_request('/genres/genres/', {'page[number]': 1, 'page[size]': 20})
    # Проверка результата
    assert response.status == 200
    assert len(response.body) >= 1

    response = await make_get_request('/genres/genres/')
    assert response.status == 200

@pytest.mark.asyncio
async def test_genres_detail_valid_data(make_get_request):
    """Тест проверяет работу получения по id в эндпоинте genres"""
    response = await make_get_request('/genres/6c162475-c7ed-4461-9184-001ef3d9f26e')
    genre_data = {
        "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
        "genre": "Sci-Fi"
        }
    assert response.status == 200
    assert response.body == genre_data

@pytest.mark.asyncio
async def test_validator_1(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/genres/genres/', {'page[number]': 0})
    assert response.status == 422

@pytest.mark.asyncio
async def test_validator_2(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/genres/genres/', {'page[size]': 0})
    assert response.status == 422

@pytest.mark.asyncio
async def test_validator_3(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/genres/1-not-valid-uuid')
    assert response.status == 404

@pytest.mark.asyncio
async def test_validator_4(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request('/genres/1')
    assert response.status == 404
