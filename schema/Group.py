from pydantic import BaseModel,EmailStr

class GroupCreate(BaseModel):
    name:str


class AddUser(BaseModel):
    email:EmailStr