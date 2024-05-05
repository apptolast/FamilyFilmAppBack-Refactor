from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Language(Base):
    __tablename__ = 'Language'
    id = Column(Integer, primary_key=True)
    language = Column(String)

    users = relationship("User", back_populates="language")
