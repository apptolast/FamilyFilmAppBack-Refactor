from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchemaRequest(BaseModel):
    name:str

class UserSchemaResponse(BaseModel):
    
    id:int
    owner_id:int
    name: str
    provider:str

