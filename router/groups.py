from fastapi import APIRouter,Depends
from config.db import session
from controllers.Group import GroupService
from router.users import UserServiceRepository
from schema.Group import GroupSchemaRequest

router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)

GroupRepository = GroupService(db_session= session)

@router.post("")
async def create_group(group:GroupSchemaRequest,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']))
    return GroupRepository.create_group(name = group.name,ownerID = user.id)

@router.get("")
async def get_groups(me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']))
    return GroupRepository.get_groups(user_id= user.id)

@router.get("/{id}")
async def get_groups(id:int,me = Depends(UserServiceRepository.auth_user)):
    return GroupRepository.get_group_id(id)