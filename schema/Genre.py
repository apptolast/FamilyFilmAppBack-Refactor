from pydantic import BaseModel

class GenreResponse(BaseModel):
    id:int
    name:str