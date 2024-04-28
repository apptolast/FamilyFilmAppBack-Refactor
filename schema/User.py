from pydantic import BaseModel, EmailStr, validator
from  controllers.users import pwd_context
from typing import Optional,List


class User(BaseModel):
    userId:int
    email:EmailStr
    provider: Optional[str]
    role:str

class userCreate(BaseModel):
    email:EmailStr
    provider:str
    


class UserData(BaseModel):
    userId:int
    groupId: List[int] = []
    user:User

