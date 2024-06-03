from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import Base



class MovieUserGroup(Base):
    __tablename__ = 'Movie_User_Group'
    id = Column(Integer, primary_key=True)
    id_movie = Column(Integer, ForeignKey('Movie.id'), nullable=False)
    id_user = Column(Integer, ForeignKey('User.id'), nullable=False)
    id_group = Column(Integer, ForeignKey('Group.id'), nullable=False)
    toWatch = Column(Boolean, nullable=True)

    movie = relationship("Movie", back_populates="group_associations")
    user = relationship("User", back_populates="group_associations")
    group = relationship("Group", back_populates="group_associations")