from config.db import session
from models.Genre import Genre
from sqlalchemy import text


def genre_filter(idiom,name):
    return session.query(Genre).filter(text(f"genres.name->>'{idiom}' = :name")).params(name=name).first()


def get_all_genres():
    return session.query(Genre).all()

def get_genre_by_id(id):
    return session.query(Genre).filter(Genre.id == id).first()