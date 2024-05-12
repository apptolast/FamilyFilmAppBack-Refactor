from typing import Optional
from pydantic import BaseModel, EmailStr 
from schema.User import UserSchemaResponse


class GroupSchemaRequest(BaseModel):
    name:str

class UserSchemaResponse(BaseModel):
    
    id:int
    owner_id:int
    name: str
    provider:str


class usuarito(BaseModel):
    
    id:int
    email: EmailStr
    language:Optional[int] = None
    provider:str

class groupSchema(BaseModel):
    id:int
    owner_id:int
    name:str
    users:list[usuarito]