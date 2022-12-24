import pytest


@pytest.mark.asyncio
async def test_genre_all_valid_data(prepare_data, make_get_request):
    # Выполнение запроса
    response = await make_get_request('/genre/', {'page': 1, 'size': 20})
    # Проверка результата
    assert response.status == 200
    assert len(response.body) >= 1

    response = await make_get_request('/genre/')
    assert response.status == 200, 'not work with default params page=1, size=50'


@pytest.mark.asyncio
async def test_genre_all_not_valid_params(prepare_data, make_get_request):
    # Выполнение запроса

    response = await make_get_request('/genre', {'page': 0})
    assert response.status == 422, 'too small page validator, status must be 422'

    response = await make_get_request('/genre', {'size': 2001})
    assert response.status == 422, 'too large size validator, status must be 422'

    response = await make_get_request('/genre', {'size': 0})
    assert response.status == 422, 'too small size validator, status must be 422'


@pytest.mark.asyncio
async def test_genre_detail_valid_data(prepare_data, make_get_request):
    response = await make_get_request('/genre/e91db2b1-d967-4785-bec9-1eade1d56243')
    assert response.status == 200
    assert response.body == prepare_data[0]

    response = await make_get_request('/genre/4bas47a2-4dq0-2bq6-c35b-12fa24hf3cbe')
    assert response.status == 404, 'not found genre, status must be 404'


@pytest.mark.asyncio
async def test_genre_detail_not_valid_data(prepare_data, make_get_request):
    response = await make_get_request('/genre/1-not-valid-uuid')
    assert response.status == 422, "not valid genre_id status must be 422"

    response = await make_get_request('/genre/1')
    assert response.status == 422, "not valid genre_id status must be 422"
