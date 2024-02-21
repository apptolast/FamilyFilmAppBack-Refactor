from fastapi import APIRouter, HTTPException,status,Depends
from models import WatchList, ViewList
from models.GroupUser import GroupUser
from schema.Group import GroupCreate,AddUser,GroupData,WatchListCreate,ViewListCreate
from config.db import session
from models.Group import Group
from controllers.users import auth_user
from models.User import User
from controllers.groups import GroupData_id, get_group_all, get_group_by_id
from controllers.session import add_to_db,delete_to_db
from schema.Movie import ShowMovie, movieData
router = APIRouter(
    prefix="/group",
    tags=["Groups"]
)

@router.post("/create/{idiom:str}", status_code=201,response_model= GroupData,)
async def create_group(idiom:str,group: GroupCreate,me = Depends(auth_user)):
    new_group = Group(name= group.name)
    add_to_db(new_group)
    db_groupUser = GroupUser(user_id = me.id, group_id =new_group.id)
    add_to_db(db_groupUser)
    return GroupData_id(new_group.id,idiom)

@router.get('/all/{idiom:str}')
async def get_groups(idiom:str):
    return [GroupData_id(group.id, idiom) for group in get_group_all()]

@router.get('/{id:int}/{idiom:str}',status_code=200,response_model=GroupData)
async def get_group(idiom:str,id:int):
    return GroupData_id(id,idiom)

@router.patch('/edit/{id:int}/{idiom:str}',response_model=GroupData, status_code=201)
async def edit_group(idiom:str,group:GroupCreate,id:int,me = Depends(auth_user)):
    if GroupData_id(id,idiom).user_owner_id == me.id:
        try:
            session.query(Group).filter(Group.id == id).update(dict(group))
            session.commit()
        except Exception as e:
            return e 
        return GroupData_id(id,idiom)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not admin")
        
@router.patch('/adduser/{id:int}/{idiom:str}',status_code=200,response_model=GroupData)
async def add_user_to_group(idiom:str,user:AddUser,id:int,me = Depends(auth_user)):
     group = get_group_by_id(id)
     user_real = session.query(User).filter(User.email == user.email).first()
     add_to_db(GroupUser(user_id= user_real.id, group_id=group.id))
     return GroupData_id(id,idiom)

@router.patch('/deleteuser/{id:int}/{idiom:str}',status_code=200,response_model=GroupData)
async def delete_user_from_group(user:AddUser,id:int,idiom:str,me = Depends(auth_user)):
     group = get_group_by_id(id)
     user_real = session.query(User).filter(User.email == user.email).first()
     delete_to_db(session.query(GroupUser).filter_by(user_id=user_real.id, group_id=group.id).first())
     return GroupData_id(id,idiom)
    
@router.delete('/delete/{id:int}/{idiom:str}',status_code=200, response_model=GroupData)
async def delete_group(id:int,idiom:str, me = Depends(auth_user)):
    group_rip = GroupData_id(id,idiom)
    delete_to_db(get_group_by_id(id))
    return group_rip

@router.patch('/addWatch/{idiom:str}')
async def add_WatchList_to_group(WatchListCreate:WatchListCreate,idiom:str):
    add_to_db(WatchList(**dict(WatchListCreate)))
    return GroupData_id(WatchListCreate.group_id, idiom)

@router.delete('/DeleteWatch/{idiom:str}')
async def delete_WatchList_to_group(WatchListCreate:WatchListCreate,idiom:str):
    delete_to_db(session.query(WatchList).filter(WatchList.movie_id == WatchListCreate.movie_id).first())
    return GroupData_id(WatchListCreate.group_id, idiom)

@router.patch('/addViewList/{idiom:str}')
async def add_ViewList_to_group(ViewListCreate:ViewListCreate,idiom:str):
    add_to_db(ViewList(**dict(ViewListCreate)))
    return GroupData_id(ViewListCreate.group_id, idiom)

@router.delete('/addViewList/{idiom:str}')
async def delete_ViewList_to_group(ViewListCreate:ViewListCreate,idiom:str):
    delete_to_db(session.query(ViewList).filter(ViewList.movie_id == ViewListCreate.movie_id).first())
    return GroupData_id(ViewListCreate.group_id, idiom)