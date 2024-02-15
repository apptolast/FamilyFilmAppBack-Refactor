from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    movies = Column(list)

class GenreMovie(Base):
    __tablename__ = "genre_movies"

    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)

    genre = Column(list)
    movie = Column(list)

