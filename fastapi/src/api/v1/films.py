from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from core.exception_detail import ExceptionDetail
from services.film import FilmService, get_film_service
from models.film import Film

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=Film,
    summary="Поиск кинопроизведений по id",
    description="поиск кинопроизведений по id",
    response_description="Название и рейтинг фильма",
)
async def film_details(
    film_id: str = Query(default="0312ed51-8833-413f-bff5-0e139c11264a"),
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    film = await film_service.get_by_id("movies", film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ExceptionDetail.FilmDetails)

    return Film(id=film.id, title=film.title, imdb_rating=film.imdb_rating)


@router.get(
    "/movies/",
    response_model=List[Film],
    summary="Поиск кинопроизведений по страницам",
    description="поиск списка кинопроизведений по номеру страницы",
    response_description="Список с названием и рейтингом фильма",
)
async def movies_details(
    rating_filter: float = None,
    sort: bool = False,
    page_number: int = Query(default=1, alias="page[number]", ge=1),
    page_size: int = Query(default=20, alias="page[size]", ge=1),
    film_service: FilmService = Depends(get_film_service),
) -> List[Film]:

    films = await film_service.get_page_number("movies", rating_filter, sort, page_number, page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ExceptionDetail.MoviesDetails)

    return films


@router.get("/search/", response_model=List[Film], summary="Search films", description="Search films by provided query")
async def search_films(
    query: str = None,
    sort: bool = False,
    page_number: int = Query(default=1, alias="page[number]", ge=1),
    page_size: int = Query(default=20, alias="page[size]", ge=1),
    film_service: FilmService = Depends(get_film_service),
) -> List[Film]:
    """Осуществляет поиск фильмов по базе и возвращает список с подходящими фильмами,
    учитывая пагинацию"""
    films = await film_service.get_request(
        "movies",
        query,
        sort,
        page_number,
        page_size,
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ExceptionDetail.MoviesDetails)

    return films
