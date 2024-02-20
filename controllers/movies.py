from controllers.moviesapi import api,base_url_movies,adult,video
from controllers.session import add_to_db
from models.Movie import Movie
from config.db import session

def downloadMovie(language: str):
    # Usa la base_url_movies y agrega el parámetro de página
    first_page_results = api(f"{base_url_movies}&page=1")
    first_page = first_page_results['total_pages']
    first_results = first_page_results['results']
    
    for movie in first_results:
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
            vote_count=movie['vote_count']))

    for actual_page in range(2, first_page + 1):
        # Actualiza la URL con la página actual antes de hacer la llamada a la API
        current_page_results = api(f"{base_url_movies}&page={actual_page}")
        
        for movie in current_page_results['results']:
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
                vote_count=movie['vote_count']))

    if video:
        return downloadMovie(language, adult, video=False)

    elif adult:
        return downloadMovie(language, adult=False, video=True)
    
    return session.query(Movie).all()