from sqlalchemy import Column, Integer, String, relationship
from sqlalchemy.orm import backref
from models.base import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    users = relationship(
        "User",
        secondary="group_users",
        backref=backref("groups", lazy="dynamic"),
        cascade="all, delete-orphan"
    )

    watchList = relationship("WatchList", backref="group")
    viewList = relationship("ViewList", backref="group")
