from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    movies = relationship("GenreMovie", back_populates="genre")