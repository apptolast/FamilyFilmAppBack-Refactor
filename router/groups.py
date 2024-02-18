from fastapi import APIRouter,status,Depends
from models import WatchList, ViewList
from models.GroupUser import GroupUser
from schema.Group import GroupCreate,AddUser,GroupData
from config.db import session
from models.Group import Group
from controllers.users import auth_user
from models.User import User
from controllers.groups import GruopData_id, get_group_all, get_group_by_id,GroupData_all
from controllers.session import add_to_db,delete_to_db
from schema.Movie import ShowMovie, movieData

router = APIRouter(
    prefix="/group",
    tags=["Groups"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model= GroupData )
async def create_group(group: GroupCreate,me = Depends(auth_user)):
    add_to_db(Group(name= group.name))
    db_groupUser = GroupUser(user_id = me.id, group_id =get_group_all()[-1].id)
    add_to_db(db_groupUser)
    return GruopData_id(get_group_all()[-1].id)

@router.get('/all')
async def get_groups(me = Depends(auth_user)):
    return GroupData_all()

@router.get('/{id:int}')
async def get_group(id:int,me = Depends(auth_user)):
        return GruopData_id(id)

@router.patch('/edit/{id:int}')
async def edit_group(group:GroupCreate,id:int,me = Depends(auth_user)):
    
    if session.query(GroupUser).filter((GroupUser.user_id == me.id) & (GroupUser.group_id == id)).first() == None:
         return "No"
    try:
        session.query(Group).filter(Group.id == id).update(dict(group))
        session.commit()
    except Exception as e:
        return e 
    return get_group_by_id(id)


@router.patch('/adduser/{id:int}')
async def add_user_to_group(user:AddUser,id:int,me = Depends(auth_user)):
     group = get_group_by_id(id)
     add_to_db(group.users.append(GroupUser(user_id=session.query(User).filter(User.email == user.email).first().id, group_id=group.id)))
     return get_group_by_id(id).users
     

@router.delete('/delete/{id:int}')
async def delete_group(id, me = Depends(auth_user)):
     delete_to_db(get_group_by_id(id))