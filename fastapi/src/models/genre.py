from typing import Optional

from models.base_model import ESModel


class Genre(ESModel):
    id: str
    genre: str


class ESGenre(ESModel):
    id: str
    genre: str
    description: Optional[str]
