from fastapi import HTTPException
from sqlalchemy import text
from controllers.moviesapi import api,base_url_movies,video,adult
from controllers.session import add_to_db
from models.Movie import Movie
from config.db import session
from schema.Movie import MovieCreate
from fastapi import status

def downloadMovie(language: str,page:int, adult = adult,video= video):
    if page > 500:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="the page limit is 500 :(")
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

def get_all_movies(idiom, page=1, items_per_page=20):
    start = (page - 1) * items_per_page
    end = start + items_per_page
    movies = session.query(Movie.id, text(f"movies.title->>'{idiom}'")).slice(start, end).all()
    list_movie = []
    for movie in movies:
        if movie[1] is None:
            continue
        list_movie.append(get_movie_by_id(movie.id,idiom))
    contador = page + 1
    if len(list_movie) < 19:
        downloadMovie(idiom,contador)
        return get_all_movies(idiom,contador)
    return {f"peliculas mostrando : {len(list_movie)}":list_movie}

def get_movie_by_id(id, idiom):
    movie = session.query(Movie).filter(Movie.id == id).first()
    if movie is not None:
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
    return ""
   