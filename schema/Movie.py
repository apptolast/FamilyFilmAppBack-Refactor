from pydantic import BaseModel,validator

class MovieCreate(BaseModel):
    id: int
    adult: bool = False
    title: str
    genre_ids: list[int]
    language: str
    synopsis: str
    image: str | None = None
    release_date: str | None = None
    vote_average: float | None = None
    vote_count: int | None = None

    @validator("genre_ids")
    def at_least_one_genre(cls, v):
        if not v or len(v) < 1:
            raise ValueError("At least one genre must be specified.")
        return v



class ShowMovie(BaseModel):
    id: int
    adult: bool = False
    title: str
    genre_ids: list[int]
    language: str
    synopsis: str
    image: str | None = None
    release_date: str | None = None
    vote_average: float | None = None
    vote_count: int | None = None