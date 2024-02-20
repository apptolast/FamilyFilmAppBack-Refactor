from sqlalchemy import text
from controllers.moviesapi import api,base_url_movies,video,adult
from controllers.session import add_to_db
from models.Movie import Movie
from config.db import session

def downloadMovie(lenguage: str):

    for page in range(1, api(base_url_movies)["total_pages"] + 1):
        for movie in api(f"{base_url_movies}&page={page}")['results']:

            existing_movie = get_movie_by_id(movie['id'],lenguage)
            if get_movie_by_id(movie['id'],lenguage):
                existing_movie['title'][lenguage] = movie['title']
                existing_movie['synopsis'][lenguage] = movie['overview']
                session.commit()
            
            add_to_db(Movie(
                id=movie['id'],
                adult=movie['adult'],
                title={lenguage: movie['title']},
                genre_ids=movie['genre_ids'],
                language=movie['original_language'],
                synopsis={lenguage: movie['overview']},
                image=movie['poster_path'],
                release_date=movie['release_date'],
                vote_average=movie['vote_average'],
                vote_count=movie['vote_count']))

    if video:
        return downloadMovie(lenguage, adult, video=False)

    elif adult:
        return downloadMovie(lenguage, adult=False, video=True)
    
    return session.query(Movie).all()

def get_all_movies(idiom, page=1, items_per_page=100):
    start = (page - 1) * items_per_page
    end = start + items_per_page
    movies = session.query(Movie.id, text(f"movies.title->>'{idiom}'")).slice(start, end).all()
    return [{'id': movie[0], 'title': movie[1]} for movie in movies]

def get_movie_by_id(id, idiom):
    movie = session.query(Movie.id, text(f"movies.title->>'{idiom}'")).filter(Movie.id == id).first()
    return {'id': movie[0], 'title': movie[1]} if movie else None