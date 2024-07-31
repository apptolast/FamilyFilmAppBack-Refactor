import os
from controllers.Genre import GenreService
from fastapi import HTTPException,status
import requests
from models.GenreMovie import GenreMovie
from models.Movie import Movie
from models.Language import Language
from schema.Movie import MovieResponse
from sqlalchemy import func, text

class MovieService:


    def __init__(self,db_session):
        self.db_session = db_session
    

    def get_movies(self,page,language):
        
        items_per_page = 20
        start = (page - 1) * items_per_page
        end = start + items_per_page

        try:
            movies = self.db_session.query(Movie).slice(start, end).all()
                   
            if len(movies) < items_per_page:
                self.download_movie(language,page)
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
    
    def download_movie(self, language, page, adult=True, video=True):
        if page > 500:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The page limit is 500")

        movie_downloads = []
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult={adult}&include_video={video}&language={language}&sort_by=popularity.desc&page={page}"

        response = self.api_start(url)
        movies = response.get('results', [])

        for movie in movies:
            existing_movie = self.db_session.query(Movie).filter(Movie.id == movie['id']).first()
            
            if existing_movie is None:
                new_movie = Movie(
                    id=movie['id'],
                    title={f"{language}": movie['title']},
                    synopsis={f"{language}": movie['overview']},
                    image=movie['poster_path'],
                    adult=movie['adult'],
                    release_date=movie['release_date'],
                    rating_average=movie['vote_average'],
                    rating_value=movie['vote_count']
                )
                self.db_session.add(new_movie)
                self.db_session.commit()

                movie_downloads.append(new_movie)
            else:
                existing_movie.title = {**existing_movie.title, language: movie['title']}
                existing_movie.synopsis = {**existing_movie.synopsis, language: movie['overview']}
                self.db_session.commit()

            try:
                self.db_session.commit()
            except Exception as e:
                self.db_session.rollback()
            
            movie_downloads.append(movie)

        if video:
            return self.download_movie(language, page, video=False, adult=adult)
        elif adult:
            return self.download_movie(language, page, video=video, adult=False)

        return {len(movie_downloads):movie_downloads}
    
    def download_movie_by_name(self, language, name , page, adult=True):
        if page > 500:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The page limit is 500")

        movie_downloads = []
        url = f"https://api.themoviedb.org/3/search/movie?query={name}&include_adult={adult}&{language}=es&page={page}"

        response = self.api_start(url)
        movies = response.get('results', [])

        for movie in movies:
            existing_movie = self.db_session.query(Movie).filter(Movie.id == movie['id']).first()
            
            if existing_movie is None:
                new_movie = Movie(
                    id=movie['id'],
                    title={f"{language}": movie['title']},
                    synopsis={f"{language}": movie['overview']},
                    image=movie['poster_path'],
                    adult=movie['adult'],
                    release_date=movie['release_date'],
                    rating_average=movie['vote_average'],
                    rating_value=movie['vote_count']
                )
                self.db_session.add(new_movie)
                self.db_session.commit()

                movie_downloads.append(new_movie)
            else:
                existing_movie.title = {**existing_movie.title, language: movie['title']}
                existing_movie.synopsis = {**existing_movie.synopsis, language: movie['overview']}
                self.db_session.commit()

            try:
                self.db_session.commit()
            except Exception as e:
                self.db_session.rollback()
            
            movie_downloads.append(movie)

        if adult:
            return self.download_movie_by_name(language, name ,page, adult=False)

        return movie_downloads
    
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

    def movie_by_name(self,name,language):
        # Construir la consulta para extraer el texto del campo JSON `title` en el idioma especificado
        movies = (
            self.db_session.query(Movie)
            .filter(
                func.json_extract_path_text(Movie.title, language).ilike(f"%{name}%")
            )
            .all()
        )
        
        return movies
    

    def api_start(self,url):
        return requests.get(url, headers={
            "accept": "application/json",
            "Authorization": os.getenv('header_authorization')
        }).json()

    def get_movie_or_none(self, id: int, language: str):
        # Obtener la película desde el repositorio
        movie = self.get_movie_id(id)
        
        # Verificar si la película existe
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        
        # Obtener los géneros asociados con la película
        genres_in_movie = self.db_session.query(GenreMovie).filter(GenreMovie.id_movie == movie.id).all()
        genres_name = [GenreService(self.db_session).get_genre(language, genre.id_genre).name for genre in genres_in_movie]
        
        # Verificar que el título y la sinopsis existen en el idioma solicitado
        if not movie.title.get(language) or not movie.synopsis.get(language):
            return None
        
        # Retornar la respuesta de la película
        return MovieResponse(
            id=movie.id,
            title=movie.title[language],
            synopsis=movie.synopsis[language],
            image=movie.image,
            adult=movie.adult,
            release_date=movie.release_date,
            rating_average=movie.rating_average,
            rating_value=movie.rating_value,
            genres=genres_name,
        )


