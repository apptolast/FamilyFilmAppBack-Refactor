from pydantic import BaseModel

class GroupCreate(BaseModel):
    name:str
