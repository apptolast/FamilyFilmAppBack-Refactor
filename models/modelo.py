from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class MovieUserGroup(Base):
    __tablename__ = 'Movie_User_Group'
    id_movie = Column(Integer, ForeignKey('Movie.id'), primary_key=True)
    id_user = Column(Integer, ForeignKey('User.id'), primary_key=True)
    id_group = Column(Integer, ForeignKey('Group.id'), primary_key=True)
    toWatch = Column(Boolean)

    movie = relationship("Movie", back_populates="group_associations")
    user = relationship("User", back_populates="group_associations")
    group = relationship("Group", back_populates="group_associations")
