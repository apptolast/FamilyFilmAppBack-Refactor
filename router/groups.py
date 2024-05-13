from fastapi import APIRouter,Depends
from pydantic import EmailStr
from config.db import session
from controllers.DataTransfer import DataTransfer
from controllers.Group import GroupService
from controllers.MovieGroupUser import MovieUserGroupService
from router.users import UserServiceRepository
from schema.Group import GroupSchemaRequest, groupSchemaDeleteUser

router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)

GroupRepository = GroupService(db_session= session,movie_user_group_repository=MovieUserGroupService(db_session=session))
returns = DataTransfer()
@router.post("")
async def create_group(group:GroupSchemaRequest,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    GroupRepository.create_group(name = group.name,ownerID = user.id)
    return returns.get_groups(user.id)

@router.post("/{group_id}/user/{user_id}")
async def group_add_user(user_id:int,group_id:int,me = Depends(UserServiceRepository.auth_user)):
    # correo electronico, no id
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return GroupRepository.add_user_to_group(user_id,group_id,user.id)

@router.get("")
async def get_groups(me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return returns.get_groups(user.id)

@router.get("/{id}")
async def get_group(id:int,me = Depends(UserServiceRepository.auth_user)):
    return returns.get_group(id)

@router.delete("/{group_id}/user")
async def group_delete_user(user_to_delete_email:groupSchemaDeleteUser,group_id:int,me = Depends(UserServiceRepository.auth_user)):
    user_owner = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    user_to_delete = UserServiceRepository.check_user_exists(user_to_delete_email.email).id
    return GroupRepository.delete_user_to_group(user_to_delete,group_id,user_owner.id)

@router.delete("/{group_id}")
async def group_delete_with_users(group_id,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    GroupRepository.delete_user_and_group(users_id=returns.get_group(group_id).users,group_id=group_id,owner_id=user.id)
    return returns.get_groups(user.id)
