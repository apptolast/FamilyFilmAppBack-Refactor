from controllers.Movie import  MovieService
from controllers.Genre import GenreService
from config.db import session
from models.GenreMovie import GenreMovie
from schema.Movie import MovieResponse

class DataTransfer:

    MovieServiceRepository = MovieService(session)
    GenreServiceRepository = GenreService(session)
    session = session
 
    def get_movie_datatransfer(self,id,language):
        movie = self.MovieServiceRepository.get_movie(id)
        genres_in_movie = session.query(GenreMovie).filter(GenreMovie.id_movie == movie.id).all()
        genres_name = [self.GenreServiceRepository.get_genre(language,genre.id_genre).name for genre in genres_in_movie]
        return MovieResponse(
                id = movie.id,
                title = movie.title[language],
                synopsis = movie.synopsis[language],
                image = movie.image,
                adult = movie.adult,
                release_date = movie.release_date,
                rating_average = movie.rating_average,
                rating_value = movie.rating_value,
                genres = genres_name,
        )
    
    def get_movies_datatransfer(self,language,page):
        movies = self.MovieServiceRepository.get_movies(language,page)
        movies_response = []
        for movie in movies:
            genres_in_movie = session.query(GenreMovie).filter(GenreMovie.id_movie == movie.id).all()
            genres_name = [self.GenreServiceRepository.get_genre(language,genre.id_genre).name for genre in genres_in_movie]
            movies_response.append(
                MovieResponse(
                id = movie.id,
                title = movie.title[language],
                synopsis = movie.synopsis[language],
                image = movie.image,
                adult = movie.adult,
                release_date = movie.release_date,
                rating_average = movie.rating_average,
                rating_value = movie.rating_value,
                genres = genres_name,
        ))
        return movies_response