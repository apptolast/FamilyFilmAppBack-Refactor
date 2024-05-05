from typing import List
from fastapi import APIRouter,Depends
from schema.User import UserSchemaRequest, UserSchemaResponse
from controllers.User import UserService
from config.db import session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

UserServiceRepository = UserService(session)

@router.get('', status_code=200, response_model=List[UserSchemaResponse])
async def get_users(me = Depends(UserServiceRepository.auth_user)):
    users = UserServiceRepository.get_users()
    return [UserSchemaResponse(
        id= user.id,
        email =  user.email,
        provider =user.provider,
        language = user.id_language
        ) for user in users]

@router.get('/{id:int}',status_code=200)
async def get_user(id:int, me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(id)
    return UserSchemaResponse(
        id= user.id,
        email =  user.email,
        provider =user.provider,
        language = user.id_language
        )

@router.get('/me',status_code=200,response_model=UserSchemaResponse)
async def me(me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(me.id)
    return UserSchemaResponse(
        id= user.id,
        email =  user.email,
        provider =user.provider,
        language = user.id_language
        )


@router.delete('',status_code=204)
async def delete_user(me = Depends(UserServiceRepository.auth_user)):
    UserServiceRepository.delete_user(me)