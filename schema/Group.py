from typing import Optional
from pydantic import BaseModel, EmailStr

from schema.Movie import MovieResponse


class GroupSchemaRequest(BaseModel):
    name:str

class UserSchemaResponse(BaseModel):
    
    id:int
    owner_id:int
    name: str
    provider:str


class groupSchema(BaseModel):
    id:int
    owner_id:int
    users:list[EmailStr]
    movie_toWatch:list[MovieResponse]
    movie_Watched:list[MovieResponse]