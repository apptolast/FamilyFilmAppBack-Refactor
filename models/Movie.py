from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from models.base import Base
from models.GenreMovieAssociation import genre_movie_association

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    adult = Column(Boolean, default=False)
    title = Column(String)
    genre_ids = Column(ARRAY(Integer))
    language = Column(String)
    synopsis = Column(String, nullable=True)
    image = Column(String, nullable=True)
    release_date = Column(String, nullable=True)  # Ajustado a String para mantener la consistencia con Prisma
    vote_average = Column(Float)
    vote_count = Column(Integer, nullable=True)

    genres = relationship('Genre', secondary=genre_movie_association, back_populates='movies')
    watchLists = relationship('WatchList', back_populates='movie')
    viewLists = relationship('ViewList', back_populates='movie')