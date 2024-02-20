from sqlalchemy import JSON, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from models.base import Base
from models.GenreMovieAssociation import genre_movie_association

class Movie(Base):
    __tablename__ = 'movies'


    id = Column(Integer, primary_key=True, autoincrement=True)
    adult = Column(Boolean, default=False)
    title = Column(JSON)
    genre_ids = Column(ARRAY(Integer))
    language = Column(String)
    synopsis = Column(JSON, nullable=True)
    image = Column(String, nullable=True)
    release_date = Column(String, nullable=True) 
    vote_average = Column(Float)
    vote_count = Column(Integer, nullable=True)

    genres = relationship('Genre', secondary=genre_movie_association, back_populates='movies')
    watchLists = relationship('WatchList', back_populates='movie')
    viewLists = relationship('ViewList', back_populates='movie')

    #"overview": "After a deadly earthquake turns Seoul into a lawless badland, a fearless huntsman springs into action to rescue a teenager abducted by a mad doctor.",
    # "title": "Badland Hunters",
