from fastapi import APIRouter,status
from sqlalchemy.exc import IntegrityError
from schema.Group import GroupCreate
from config.db import session
from models.Group import Group


router = APIRouter(
    prefix="/group",
    tags=["Groups"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_group(group: GroupCreate):
    db_group = Group(name= group.name, users = [],watchList = [], viewList = [])
    session.add(db_group)
    session.commit()

    return {"status": "success", "data": db_group}

@router.get('/all')
async def get_groups():
    return session.query(Group).all()

@router.get('/{id:int}')
async def get_group(id:int):
        return session.query(Group).filter(Group.id == id).first()

@router.patch('/edit/{id:int}')
async def edit_group(group:GroupCreate,id:int):
     try:
        session.query(Group).filter(Group.id == id).update(dict(group), synchronize_session=False)
     except IntegrityError:
        session.rollback()
        return 'error'
     session.commit()
     return session.query(Group).filter(Group.id == id).first()


