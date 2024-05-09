from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchemaRequest(BaseModel):
    email: EmailStr
    provider:str
    
class UserFirebaseBackendTestRequest(BaseModel):
    email: EmailStr
    email_verified: Optional[bool] = True
    password: str

class UserTokenResponse(BaseModel):
    token:str

class UserSchemaResponse(BaseModel):
    
    id:int
    email: EmailStr
    language:Optional[int] = None
    provider:str