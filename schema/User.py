from pydantic import BaseModel, EmailStr, validator
from  controllers.users import pwd_context

class userCreate(BaseModel):
    email:EmailStr
    firebase_uuid:str

    @validator("firebase_uuid")
    def hash_password(cls, firebase_uuid):
        return pwd_context.hash(firebase_uuid)
    

class userLogin(userCreate):
    @validator("firebase_uuid")
    def hash_password(cls, firebase_uuid):
        return firebase_uuid