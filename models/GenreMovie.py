from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class GenreMovie(Base):
    __tablename__ = "genre_movies"

    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)

    genre = relationship("Genre", back_populates="movies")
    movie = relationship("Movie", back_populates="genres")