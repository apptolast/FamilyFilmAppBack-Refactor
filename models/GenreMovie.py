
from sqlalchemy import Column, ForeignKey, Integer
from models.base import Base


class GenreMovie(Base):
    __tablename__ = 'Genre_Movie'
    id_genre = Column(Integer, ForeignKey('genres.id'), primary_key=True)
    id_movie = Column(Integer, ForeignKey('Movie.id'), primary_key=True)
