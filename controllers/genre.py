from config.db import session
from models.Genre import Genre
from sqlalchemy import text
from schema.Genre import ShowGenre

def genre_filter(idiom,name):
    return session.query(Genre).filter(text(f"genres.name->>'{idiom}' = :name")).params(name=name).first()

def get_all_genres(idiom):
    genres = session.query(Genre.id, text(f"genres.name->>'{idiom}'")).all()
    return [ShowGenre(id = genre[0], name = genre[1])for genre in genres]

def get_genre_by_id(id, idiom):
    genre = session.query(Genre.id, text(f"genres.name->>'{idiom}'")).filter(Genre.id == id).first()
    return ShowGenre(id = genre[0], name = genre[1]) if genre else None