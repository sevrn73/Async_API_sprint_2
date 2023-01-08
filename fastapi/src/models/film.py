from typing import Optional

from models.base_model import ESModel


class Film(ESModel):
    id: str
    title: str
    imdb_rating: Optional[float]


class ESFilm(ESModel):
    id: str
    imdb_rating: Optional[float]
    title: str
    description: Optional[str]
