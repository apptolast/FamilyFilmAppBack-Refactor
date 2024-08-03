from typing import Optional
from pydantic import BaseModel
import datetime

class MovieResponse(BaseModel):
    id:int
    title:str = None
    synopsis:str = None
    image:str = None
    adult:bool = None
    release_date: datetime.datetime = None
    rating_average:float = None
    rating_value:float = None
    genres:list[str] = None


class AutomaticResponseForMovies(BaseModel):
    download_movies: int
