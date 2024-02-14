from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    movies = relationship("GenreMovie", back_populates="genre")

class GenreMovie(Base):
    __tablename__ = "genre_movies"

    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)

    genre = relationship("Genre", back_populates="movies")
    movie = relationship("Movie", back_populates="genres")

