from typing import Optional
from pydantic import BaseModel
import datetime

class MovieResponse(BaseModel):
    id:int
    title:str
    synopsis:str 
    image:str 
    adult:bool = False
    release_date: datetime.datetime
    rating_average:float
    rating_value:float
    genres:list[str] = str



class AutomaticResponseForMovies(BaseModel):
    download_movies: int
