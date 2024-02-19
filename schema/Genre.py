from pydantic import BaseModel

class ShowGenre(BaseModel):
    id:int
    name:str