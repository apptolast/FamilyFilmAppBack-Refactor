from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class WatchList(Base):
    __tablename__ = 'watch_lists'
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)

    group = relationship('Group', back_populates='watchList')
    movie = relationship('Movie', back_populates='watchLists')