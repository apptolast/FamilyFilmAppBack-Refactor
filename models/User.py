from sqlalchemy import Column, ForeignKey, Integer, String
from models.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    id_language = Column(Integer, ForeignKey('Language.id'))
    email = Column(String, unique=True)

    language = relationship("Language", back_populates="users")
    group_associations = relationship("MovieUserGroup", back_populates="user")  # Cambiado para clarificar la relación
