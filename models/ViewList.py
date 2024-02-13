from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ViewList(Base):
    __tablename__ = "view_lists"

    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)

    group = relationship("Group", back_populates="viewList")
    movie = relationship("Movie", back_populates="viewLists")