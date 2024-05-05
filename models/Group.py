from sqlalchemy import String, Integer,Column,ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship


class Group(Base):
    __tablename__ = 'Group'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('User.id'))
    name = Column(String)

    group_associations = relationship("MovieUserGroup", back_populates="group")  # Cambiado para clarificar la relación
