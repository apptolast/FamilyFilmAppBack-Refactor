from sqlalchemy import Column, Integer, String, Boolean, Float, ARRAY
from sqlalchemy.orm import relationship
from .base import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    adult = Column(Boolean, default=False)
    title = Column(String)
    genre_ids = Column(ARRAY(Integer))
    language = Column(String)
    synopsis = Column(String)
    image = Column(String)
    release_date = Column(String)
    vote_average = Column(Float)
    vote_count = Column(Integer)

    genres = relationship("GenreMovie", back_populates="movie")
    watchLists = relationship("WatchList", back_populates="movie")
    viewLists = relationship("ViewList", back_populates="movie")