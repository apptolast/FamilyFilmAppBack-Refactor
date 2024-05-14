import logging
import os
from fastapi import HTTPException,status
import requests
from models.GenreMovie import GenreMovie
from models.Movie import Movie
from sqlalchemy import func, text

from schema.Movie import AutomaticResponseForMovies

class MovieService:

    def __init__(self,db_session):
        self.db_session = db_session
    
    def get_movies(self,page):
        
        items_per_page = 20
        start = (page - 1) * items_per_page
        end = start + items_per_page

        try:
            movies = self.db_session.query(Movie).slice(start, end).all()
            return movies
        except Exception as e:
             self.db_session.rollback()
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"No existen usuarios {e}")

    def get_movie_id(self,movie_id):
        try:
            movie = self.db_session.query(Movie).filter(Movie.id == movie_id).first()
            if not movie:
                raise HTTPException(status_code=404, detail="Movie not found")
            return movie
            
        except HTTPException as http_error:
            raise http_error

        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred:  {str(e)}")
    

    def dowload_movie(self,language,page,adult = True ,video = True):
        total_downloaded = 0
        page = 1
        while True:
            if page > 500:
                break
        
            movie_dowloads = []
            url = f"https://api.themoviedb.org/3/discover/movie?include_adult={adult}&include_video={video}&language={language}&sort_by=popularity.desc&&page={page}"
            response = self.api_start(url=url)['results']
            if not response:
                break
            for movie in response:
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
                    # Asegúrate de que el título es un diccionario
                    if isinstance(existing_movie.title, str):
                        existing_movie.title = {language: existing_movie.title}
                    existing_movie.title = {**existing_movie.title, language: movie['title']}
                    # Asegúrate de que la sinopsis es un diccionario
                    if isinstance(existing_movie.synopsis, str):
                        existing_movie.synopsis = {language: existing_movie.synopsis}
                    existing_movie.synopsis = {**existing_movie.synopsis, language: movie['overview']}
                    self.db_session.commit()
            total_downloaded += len(movie_dowloads)
            logging.info(f"{len(movie_dowloads)} movies downloaded on page {page}. Total downloaded so far: {total_downloaded}")
            page += 1
        return total_downloaded
            
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

    def update_movies(self):
        total_downloaded = 0
        languages = ["en", "es"]  # Lista de idiomas a actualizar
        for language in languages:
            downloaded = self.dowload_movie(language=language, page=1)
            total_downloaded += downloaded
            logging.info(f"Downloaded {downloaded} movies for language: {language}")
        logging.info(f"Total movies downloaded in this update: {total_downloaded}")
        return AutomaticResponseForMovies(download_movies=total_downloaded)

    def api_start(self,url):
        return requests.get(url, headers={
            "accept": "application/json",
            "Authorization": os.getenv('header_authorization')
        }).json()
