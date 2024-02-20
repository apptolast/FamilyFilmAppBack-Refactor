from controllers.moviesapi import api,video,adult,lenguage,page
from controllers.session import add_to_db
from models.Movie import Movie
from config.db import session

def downloadMovie(lenguage: str, adult=True, video=True):
    url_movies = f"https://api.themoviedb.org/3/discover/movie?include_adult={adult}&include_video={video}&language={lenguage}-US&page=1&sort_by=popularity.desc"
    total_pages = api(url_movies)["total_pages"]
    for page in range(1, total_pages + 1):
        for movie in api(f"https://api.themoviedb.org/3/discover/movie?include_adult={adult}&include_video={video}&language={lenguage}-US&page={page}&sort_by=popularity.desc")['results']:
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