from fastapi import APIRouter,Depends
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
    return returns.get_groups(user.id,returns.get_user_id(user.id).language)

@router.put("/{id}")
async def edit_group_name(id:int,group:GroupSchemaRequest,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    GroupRepository.edit_group_name(name = group.name,ownerID = user.id,group_id=id)
    return returns.get_groups(user.id,returns.get_user_id(user.id).language)


@router.get("")
async def get_groups(me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return returns.get_groups(user.id,returns.get_user_id(user.id).language)

@router.get("/{id}")
async def get_group(id:int,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return returns.get_group(id,returns.get_user_id(user.id).language)

@router.get("/groupsUser")
async def get_groups_user(me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return returns.get_all_groups_for_user(user.id, returns.get_user_id(user.id).language)
    
    
@router.delete("/{group_id}/user/{user_to_delete_id}")
async def group_delete_user(user_to_delete_id,group_id:int,me = Depends(UserServiceRepository.auth_user)):
    user_owner = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    GroupRepository.delete_user_to_group(user_to_delete_id,group_id,user_owner.id)
    return returns.get_groups(user_owner.id,returns.get_user_id(user_owner.id).language)

@router.put("/{group_id}/user")
async def group_add_user(user_add_to_group:groupSchemaDeleteUser,group_id:int,me = Depends(UserServiceRepository.auth_user)):
    user_owner = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    user_to_add = UserServiceRepository.check_user_exists(user_add_to_group.email).id
    GroupRepository.add_user_to_group(user_to_add,group_id,user_owner.id)
    return returns.get_groups(user_owner.id,returns.get_user_id(user_owner.id).language)

@router.delete("/{group_id}")
async def group_delete_with_users(group_id,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    GroupRepository.delete_user_and_group(users_id=returns.get_group(group_id,returns.get_user_id(user.id).language).users,group_id=group_id,owner_id=user.id)
    return returns.get_groups(user.id,returns.get_user_id(user.id).language)


@router.put("/{group_id}/ToWatch/{id_movie}")
async def group_add_to_watch_movie(group_id:int,id_movie:int,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    GroupRepository.add_to_watch(user.id,group_id,id_movie)
    return returns.get_groups(user.id,returns.get_user_id(user.id).language)

@router.delete("/{group_id}/ToWatch/{id_movie}")
async def group_delete_to_watch_movie(group_id:int,id_movie:int,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    GroupRepository.delete_to_watch(user.id,group_id=group_id,movie_id=id_movie)
    return returns.get_groups(user.id,returns.get_user_id(user.id).language)

@router.put("/{group_id}/ToWatched/{id_movie}")
async def group_add_to_watched_movie(group_id:int,id_movie:int,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    GroupRepository.add_to_watched(user.id,group_id,id_movie)
    return returns.get_groups(user.id,returns.get_user_id(user.id).language)

@router.delete("/{group_id}/ToWatch/{id_movie}")
async def group_delete_to_watched_movie(group_id:int,id_movie:int,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    GroupRepository.delete_to_watched(user.id,group_id=group_id,movie_id=id_movie)
    return returns.get_groups(user.id,returns.get_user_id(user.id).language)