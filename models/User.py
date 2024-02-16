from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship
from models.base import Base
from models.RoleEnum import role_enum




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    firebase_uuid = Column(String)
    role = Column(role_enum, default='USER')

    groups = relationship('GroupUser', back_populates='user')