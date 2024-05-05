from typing import List
from fastapi import APIRouter,Depends
from schema.User import UserSchemaResponse
from controllers.User import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

UserServicemethods = UserService()


# @router.get('',response_model=List[UserSchemaResponse],status_code=200)
# async def get_users(me = Depends(UserServicemethods.auth_user)):
#     return [UserSchemaResponse(user) for user in UserServicemethods.get_users()] 

@router.get('', status_code=200)
async def get_users(me = Depends(UserService.auth_user)):
    users = UserServicemethods.get_users()
    return [UserSchemaResponse(id= user.id, email= user.email) for user in users]

@router.get('/{id:int}',response_model=UserSchemaResponse,status_code=200)
async def get_user(id:int,me = Depends(UserService.auth_user)):
    return UserSchemaResponse(UserService.get_user_id(id))

# @router.get('/all',response_model=List[UserData],status_code=200)
# async def get_users():
#     return [create_userdata(user_instance) for user_instance in get_all_users()]

# @router.get('/{id:int}',response_model=UserData, status_code=200)
# async def get_user(id:int):
#         user_instance = filter_user('id',id)
#         return create_userdata(user_instance)

# @router.get('/me',status_code=200,response_model=UserData)
# async def me(user = Depends(auth_user)):
#     return create_userdata(user)