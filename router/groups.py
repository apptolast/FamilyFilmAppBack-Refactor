from fastapi import APIRouter, HTTPException,status,Depends
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
    if GruopData_id(id).user_owner_id == me.id:
        try:
            session.query(Group).filter(Group.id == id).update(dict(group))
            session.commit()
        except Exception as e:
            return e 
        return GruopData_id(id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not admin")
        
   
@router.patch('/adduser/{id:int}')
async def add_user_to_group(user:AddUser,id:int,me = Depends(auth_user)):
     group = get_group_by_id(id)
     user_real = session.query(User).filter(User.email == user.email).first()
     add_to_db(GroupUser(user_id= user_real.id, group_id=group.id))
     return GruopData_id(id)
    

@router.delete('/delete/{id:int}')
async def delete_group(id, me = Depends(auth_user)):
     delete_to_db(get_group_by_id(id))