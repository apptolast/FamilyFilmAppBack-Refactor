from fastapi import APIRouter,Depends
from controllers.users import auth_user, get_all_users,filter_user,create_userdata
from schema.User import UserData
from typing import List


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get('/all',response_model=List[UserData],status_code=200)
async def get_users():
    return [create_userdata(user_instance) for user_instance in get_all_users()]

@router.get('/{id:int}',response_model=UserData, status_code=200)
async def get_user(id:int):
        user_instance = filter_user('id',id)
        return create_userdata(user_instance)

@router.get('/me',status_code=200,response_model=UserData)
async def me(user = Depends(auth_user)):
    return create_userdata(user)