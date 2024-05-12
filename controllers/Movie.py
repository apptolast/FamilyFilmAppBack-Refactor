import os
from fastapi import HTTPException,status
import requests
from models.GenreMovie import GenreMovie
from models.Movie import Movie
from sqlalchemy import func, text

class MovieService:

    def __init__(self,db_session):
        self.db_session = db_session
    
    def get_movies(self,language,page):

        items_per_page = 20
        start = (page - 1) * items_per_page
        end = start + items_per_page
        movies = self.db_session.query(Movie).slice(start, end).all()

        if len(movies) < 20:
            self.dowload_movie(language,page=page+1)
            self.get_movies

        return movies

    def get_movie(self,id):
        return self.db_session.query(Movie).filter(Movie.id == id).first()
    

    def dowload_movie(self,language,page,adult = True ,video = True):

        if page > 500:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="the page limit is 500 ")
        
        movie_dowloads = []
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult={adult}&include_video={video}&language={language}&sort_by=popularity.desc&&page={page}"
        print(url)
        for movie in self.api_start(url)['results']:
            existing_movie = self.db_session.query(Movie).filter(Movie.id == movie['id']).first()

            if existing_movie is None:
                movie_dowloads.append(movie)
                self.db_session.add(Movie(
                    id =movie['id'],
                    title ={language: movie['title']},
                    synopsis ={language: movie['overview']},
                    image =movie['poster_path'],
                    adult =movie['adult'],
                    release_date=movie['release_date'],
                    rating_average=movie['vote_average'],
                    rating_value=movie['vote_count']
                ))
                self.db_session.commit()
                self.set_genres_with_movie(movie)
                
            else:
                existing_movie.title = {**existing_movie.title, language: movie['title']}
                existing_movie.synopsis = {**existing_movie.synopsis, language: movie['overview']}
                self.db_session.commit()
            
        if video:
            return self.dowload_movie(language, page, video=False, adult=adult)
        elif adult:
            return self.dowload_movie(language, page, video=video, adult=False)

    
                    
   
    def set_genres_with_movie(self,movie):
        genres = movie['genre_ids']
        movie_id = movie['id']

        if not self.db_session.query(GenreMovie).filter(GenreMovie.id_movie == movie_id) is None:
            
            if len(genres) == 1:
                associaton = GenreMovie(
                    id_genre = genres[0],
                    id_movie = movie_id
                )
                self.db_session.add(associaton)
                self.db_session.commit()
            else:
                for genre in genres:
                    associaton = GenreMovie(
                        id_genre = genre,
                        id_movie = movie_id
                    )
                    self.db_session.add(associaton)
                    self.db_session.commit()

    def api_start(self,url):
        return requests.get(url, headers={
            "accept": "application/json",
            "Authorization": os.getenv('header_authorization')
        }).json()
