from typing import Optional
from pydantic import BaseModel, EmailStr 



class GroupSchemaRequest(BaseModel):
    name:str

class usuarito(BaseModel):
    id:int
    email: EmailStr
    language:Optional[str] = None
    provider:str

class groupSchema(BaseModel):
    id:int
    owner_id:int
    name:str
    users:list[usuarito]

class groupSchemaDeleteUser(BaseModel):
    email: str