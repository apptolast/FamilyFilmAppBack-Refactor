from fastapi import APIRouter,status
from schema.Group import GroupCreate
from config.db import session
from models.Group import Group
router = APIRouter(
    prefix="/group"
)



@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_group(group: GroupCreate):
    db_group = Group(**dict(group))
    session.add(db_group)
    session.commit()

    return {"status": "success", "data": db_group}