from sqlalchemy import text
from controllers.moviesapi import api,base_url_movies,video,adult
from controllers.session import add_to_db
from models.Movie import Movie
from config.db import session
from schema.Movie import MovieCreate

def downloadMovie(language: str,page:int):
    cantidad_peliculas = 0
    url = base_url_movies(adult,video,language)
    for movie in api(f"{url}&page={page}")['results']:
        cantidad_peliculas += 1
        existing_movie = session.query(Movie).filter(Movie.id == movie['id']).first()
    
        if existing_movie is None:
            add_to_db(Movie(
                id=movie['id'],
                adult=movie['adult'],
                title={language: movie['title']},
                genre_ids=movie['genre_ids'],
                language=movie['original_language'],
                synopsis={language: movie['overview']},
                image=movie['poster_path'],
                release_date=movie['release_date'],
                vote_average=movie['vote_average'],
                vote_count=movie['vote_count']
            ))
    
        else:
            existing_movie.title = {**existing_movie.title, language: movie['title']}
            existing_movie.synopsis = {**existing_movie.synopsis, language: movie['overview']}
            session.commit()
    
    if video:
        return downloadMovie(language, page, video=False, adult=adult)
    elif adult:
        return downloadMovie(language, page, video=video, adult=False)

    

    return {"message":f"download great! {cantidad_peliculas}"}

def movie_with_genre(genre,page,idiom,items_per_page = 20):
    start = (page - 1) * items_per_page
    end = start + items_per_page
    return [get_movie_by_id(pelicula._asdict()['id'],idiom) for pelicula in session.query(Movie.id, text("movies.title->>'es'")).filter(Movie.genre_ids.contains([int(genre)])).slice(start, end).all() ]


def get_all_movies(idiom, page=1, items_per_page=20):
    start = (page - 1) * items_per_page
    end = start + items_per_page
    movies = session.query(Movie.id, text(f"movies.title->>'{idiom}'")).slice(start, end).all()
    if [{'id': movie[0], 'title': movie[1]} for movie in movies] == 0:
        downloadMovie(idiom,1)
        return get_all_movies(idiom,page)

def get_movie_by_id(id, idiom):
    movie = session.query(Movie).filter(Movie.id == id).first()
    print(movie)

    return MovieCreate(
            id = movie.id,
            adult = movie.adult,
            title = movie.title[idiom],
            genre_ids = movie.genre_ids,
            language = movie.language,
            synopsis = movie.synopsis[idiom],
            image = movie.image,
            release_date = movie.release_date,
            vote_average = movie.vote_average,
            vote_count = movie.vote_count
    )
   