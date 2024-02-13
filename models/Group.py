from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    users = relationship("GroupUsers", back_populates="group")
    watchList = relationship("WatchList", back_populates="group")
    viewList = relationship("ViewList", back_populates="group")