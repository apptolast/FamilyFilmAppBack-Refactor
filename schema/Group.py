from typing import Optional,Any
from pydantic import BaseModel, EmailStr
from schema.Movie import MovieResponse

class GroupSchemaRequest(BaseModel):
    name:str


class MovieGroup(BaseModel):
    id_group:int
    id_movie:int

class usuarito(BaseModel):
    id:int
    email: EmailStr
    language:Optional[str] = None
    provider:str
    movies_watch:list[MovieGroup] = []
    movies_watched:list[MovieGroup] = []


class groupSchema(BaseModel):
    id:int
    owner_id:int
    name:str
    users:list[usuarito]
    watch: list[MovieResponse] = []
    watched: list[MovieResponse] = []
    recommended_movie:Any
class groupSchemaDeleteUser(BaseModel):
    email: str