import pytest
from http import HTTPStatus


async def test_get_search(make_get_request):
    """Тест поиска записи по фразе"""
    film = {"id": "92dcddff-a70e-497c-92dc-0da12d1d528a", "title": "Exile: A Star Wars Story", "imdb_rating": 5.8}
    response = await make_get_request("/films/search/", {"query": "Exile"})
    assert response.status == HTTPStatus.OK

    assert response.body[0] == film


async def test_get_n(make_get_request):
    """Тест проверяет вывод N записей"""

    response = await make_get_request("/films/search/", {"query": "war", "page[number]": 1, "page[size]": 3})

    # Проверка результата
    assert response.status == HTTPStatus.OK

    assert len(response.body) == 3


@pytest.mark.parametrize(
    "url, expected",
    [
        (["/films/search/123"], HTTPStatus.NOT_FOUND),
        (["/films/search/", {"query": 3131}], HTTPStatus.NOT_FOUND),
        (["/films/search/", {"page[number]": 0}], HTTPStatus.UNPROCESSABLE_ENTITY),
        (["/films/search/", {"page[size]": 0}], HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
async def test_validator(make_get_request, url, expected):
    """Тест корректной валидации форм"""
    response = await make_get_request(*url)
    assert response.status == expected


async def test_redis(make_get_request):
    """Тест кэширования"""
    # этот запрос сделан без удаления кэша
    response = await make_get_request("/films/search/", {"query": "war", "page[number]": 1, "page[size]": 10}, False)
    assert response.status == HTTPStatus.OK

    response2 = await make_get_request("/films/search/", {"query": "war", "page[number]": 1, "page[size]": 10})
    assert response.status == HTTPStatus.OK

    assert response.resp_speed > response2.resp_speed
