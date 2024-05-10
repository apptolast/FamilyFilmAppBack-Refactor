from fastapi import APIRouter,Depends
from config.db import session
from controllers.Group import GroupService
from controllers.MovieGroupUser import MovieUserGroupService
from router.users import UserServiceRepository
from schema.Group import GroupSchemaRequest

router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)

GroupRepository = GroupService(db_session= session,movie_user_group_repository=MovieUserGroupService(db_session=session))

@router.post("")
async def create_group(group:GroupSchemaRequest,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return GroupRepository.create_group(name = group.name,ownerID = user.id)

@router.post("/{user_id}/{group_id}")
async def create_group(user_id:int,group_id:int,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return GroupRepository.add_user_to_group(user_id,group_id,user.id)

@router.get("")
async def get_groups(me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return GroupRepository.get_groups(user_id= user.id)

@router.get("/{id}")
async def get_groups(id:int,me = Depends(UserServiceRepository.auth_user)):
    return GroupRepository.get_group_id(id)

@router.delete("/{user_id}/{group_id}")
async def create_group(user_id:int,group_id:int,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return GroupRepository.delete_user_to_group(user_id,group_id,user.id)