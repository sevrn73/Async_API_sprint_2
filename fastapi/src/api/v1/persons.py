from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from core.exception_detail import ExceptionDetail
from services.person import PersonService, get_person_service
from models.person import ESPerson
from services.film import FilmService, get_film_service
from models.film import Film

router = APIRouter()


@router.get('/{person_id}', response_model=ESPerson)
async def person_details(
    person_id: str = Query(default='e039eedf-4daf-452a-bf92-a0085c68e156'),
    person_service: PersonService = Depends(get_person_service),
) -> ESPerson:
    person = await person_service.get_by_id('persons', person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ExceptionDetail.PersonDetails)

    return ESPerson(id=person.id, name=person.name)


@router.get('/persons/', response_model=List[ESPerson])
async def persons_details(
    sort: bool = False,
    page_number: int = Query(default=1, alias='page[number]', ge=1),
    page_size: int = Query(default=5, alias='page[size]', ge=1),
    person_service: PersonService = Depends(get_person_service),
) -> List[ESPerson]:

    persons = await person_service.get_page_number('persons', sort, page_number, page_size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ExceptionDetail.PersonsDetails)

    return persons


@router.get('/{person_id}/films', response_model=List[Film])
async def person_films(
    person_id: str = Query(default='e039eedf-4daf-452a-bf92-a0085c68e156'),
    sort: bool = False,
    page_number: int = Query(default=1, alias='page[number]', ge=1),
    page_size: int = Query(default=5, alias='page[size]', ge=1),
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service),
) -> List[Film]:

    person = await person_service.get_by_id('persons', person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ExceptionDetail.PersonDetails)

    films = await film_service.get_by_list_id('movies', person.film_ids, None, sort, page_number, page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ExceptionDetail.FilmDetails)

    return films
