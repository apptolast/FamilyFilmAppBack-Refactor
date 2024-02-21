from pydantic import BaseModel,validator

class MovieCreate(BaseModel):
    id: int
    adult: bool = False
    title: str
    genre_ids: list[int]
    language: str
    synopsis: str
    image: str 
    release_date: str 
    vote_average: float 
    vote_count: int 

    @validator("genre_ids")
    def at_least_one_genre(cls, v):
        if not v or len(v) < 1:
            raise ValueError("At least one genre must be specified.")
        return v



class ShowMovie(BaseModel):
    id: int
    adult: bool = False
    title: str
    genres: list[str]
    language: str
    synopsis: str
    image: str 
    release_date: str 
    vote_average: float 
    vote_count: int 

class movieData(BaseModel):
    group_id:int
    movie_id:int
    movie:ShowMovie
