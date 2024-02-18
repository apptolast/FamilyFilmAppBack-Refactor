from config.db import session
from models.Genre import Genre


def genre_filter(name):
    return session.query(Genre).filter(Genre.name == name).first()

def get_all_genres():
    return session.query(Genre).all()

def get_genre_by_id(id):
    return session.query(Genre).filter(Genre.id == id).first()