from sqlalchemy import ForeignKey, String, Integer, Column
from models.base import Base
from sqlalchemy.orm import relationship


class Genre(Base):
    __tablename__ = 'Genre'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    movies = relationship("Movie", secondary="Genre_Movie", back_populates="genres")
