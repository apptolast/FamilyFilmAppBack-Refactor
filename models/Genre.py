from sqlalchemy import JSON, ForeignKey, String, Integer, Column
from models.base import Base
from sqlalchemy.orm import relationship


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(JSON)


    movies = relationship("Movie", secondary="Genre_Movie", back_populates="genres")
