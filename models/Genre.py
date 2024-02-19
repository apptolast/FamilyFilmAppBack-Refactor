from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.GenreMovieAssociation import genre_movie_association


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(JSON)

    movies = relationship('Movie', secondary=genre_movie_association, back_populates='genres')
