from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship
from models.base import Base


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    users = relationship('GroupUser', back_populates='group',cascade="all, delete")
    watchList = relationship('WatchList', back_populates='group',cascade="all, delete")
    viewList = relationship('ViewList', back_populates='group',cascade="all, delete")