from fastapi import APIRouter,status,Depends
from sqlalchemy.exc import IntegrityError
from models.GroupUser import GroupUser
from schema.Group import GroupCreate
from config.db import session
from models.Group import Group
from controllers.users import auth_user
from models.User import User
from controllers.groups import get_group_all, get_group_by_id
from controllers.session import add_to_db

router = APIRouter(
    prefix="/group",
    tags=["Groups"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED, )
async def create_group(group: GroupCreate,me = Depends(auth_user)):
    db_group = Group(name= group.name)
    add_to_db(db_group)
    db_groupUser = GroupUser(user_id = me.id, group_id = get_group_all()[-1].id)
    add_to_db(db_groupUser)

    return {"status": "success", "data": f"{db_group.name} and {db_groupUser.user_id}"}

@router.get('/all')
async def get_groups(me = Depends(auth_user)):
    return get_group_all()

@router.get('/{id:int}')
async def get_group(id:int,me = Depends(auth_user)):
        return get_group_by_id(id)

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


