import pytest
from http import HTTPStatus


async def test_genres_all_valid_data(make_get_request):
    """Тест запроса для всех жанров"""
    # Выполнение запроса
    response = await make_get_request("/genres/genres/", {"page[number]": 1, "page[size]": 20})
    # Проверка результата
    assert response.status == HTTPStatus.OK
    assert len(response.body) >= 1

    response = await make_get_request("/genres/genres/")
    assert response.status == HTTPStatus.OK


async def test_genres_detail_valid_data(make_get_request):
    """Тест проверяет работу получения по id в эндпоинте genres"""
    response = await make_get_request("/genres/6c162475-c7ed-4461-9184-001ef3d9f26e")
    genre_data = {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "genre": "Sci-Fi"}
    assert response.status == HTTPStatus.OK
    assert response.body == genre_data


@pytest.mark.parametrize(
    "url, expected",
    [
        (["/genres/"], HTTPStatus.NOT_FOUND),
        (["/genres/1-not-valid-uuid"], HTTPStatus.NOT_FOUND),
        (["/genres/genres/", {"page[size]": 0}], HTTPStatus.UNPROCESSABLE_ENTITY),
        (["/genres/genres/", {"page[number]": 0}], HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
async def test_validator(make_get_request, url, expected):
    """Тест корректной валидации форм"""
    response = await make_get_request(*url)
    assert response.status == expected


async def test_validator_1(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request("/genres/genres/", {"page[number]": 0})
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_validator_2(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request("/genres/genres/", {"page[size]": 0})
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_validator_3(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request("/genres/1-not-valid-uuid")
    assert response.status == HTTPStatus.NOT_FOUND


async def test_validator_4(make_get_request):
    """Тест корректной валидации форм"""
    response = await make_get_request("/genres/1")
    assert response.status == HTTPStatus.NOT_FOUND
