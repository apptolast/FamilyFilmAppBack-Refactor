from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchemaRequest(BaseModel):
    email: EmailStr
    provider:str
    
class UserFirebaseBackendTestRequest(BaseModel):
    email: EmailStr
    email_verified: Optional[bool] = False
    phone_number: str
    password: str
    display_name: str
    photo_url: str
    disabled: Optional[bool] = False
    

class UserSchemaResponse(BaseModel):
    
    id:int
    email: EmailStr
    language:Optional[int] = None
    provider:str