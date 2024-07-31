from typing import Optional
from pydantic import BaseModel, EmailStr

from config.readJsonUsers import read_json_users_file


class UserSchemaRequest(BaseModel):
    email: EmailStr
    provider:str
    
class UserFirebaseBackendTestRequest(BaseModel):
    email: EmailStr
    email_verified: Optional[bool] = True
    password: str

class AutomaticUpdateTokenRequest(BaseModel):
    email: Optional[str] = read_json_users_file()

class AutomaticUpdateTokenResponse(BaseModel):
    email: str
    token: str

class UserTokenResponse(BaseModel):
    idToken:str
    refreshToken: str
    expiresIn: str

class UserSchemaResponse(BaseModel):
    
    id:int
    email: EmailStr
    language:Optional[str] = None
    provider:str


