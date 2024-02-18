from pydantic import BaseModel,EmailStr
from typing import Optional, List

from schema import Movie,User

class GroupCreate(BaseModel):
    name:str

class AddUser(BaseModel):
    email:EmailStr

class GroupData(GroupCreate):
    id: int
    user_owner_id: int
    watchlist: Optional[List[Movie.movieData]] = []
    viewlist: Optional[List[Movie.movieData]] = []
    users: List[User.User]