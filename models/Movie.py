from sqlalchemy import String, Integer, Boolean, Float, Date,Column
from models.base import Base
from sqlalchemy.orm import relationship


class Movie(Base):
    __tablename__ = 'Movie'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    synopsis = Column(String)
    image = Column(String)
    adult = Column(Boolean)
    release_date = Column(Date)
    rating_average = Column(Float)
    rating_value = Column(Integer)

    genres = relationship("Genre", secondary="Genre_Movie", back_populates="movies")
    group_associations = relationship("MovieUserGroup", back_populates="movie")  # Cambiado para clarificar la relación
