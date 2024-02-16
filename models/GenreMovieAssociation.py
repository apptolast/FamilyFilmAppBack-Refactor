from sqlalchemy import Column, Integer, ForeignKey, Table
from models.base import Base


genre_movie_association = Table(
    'genre_movie', Base.metadata,
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True)
)