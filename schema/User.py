from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchemaRequest(BaseModel):
    email: EmailStr
    provider:str

class UserSchemaResponse(BaseModel):
    
    id:int
    email: EmailStr
    language:Optional[str]

    class Config:
        orm_mode = True