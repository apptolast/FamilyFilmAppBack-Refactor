
from typing import Optional
from pydantic import BaseModel


class MovieUserGroup(BaseModel):
    id_movie:Optional[int] = None
    id_user:int
    id_group:int
    toWatch:Optional[bool] = None
