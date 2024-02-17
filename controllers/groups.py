

from config.db import session
from models.Group import Group

def get_group_by_id(id:int):
    return session.query(Group).filter(Group.id == id).first()

def get_group_all():
    return session.query(Group).all()