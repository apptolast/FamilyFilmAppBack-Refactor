from controllers.Auth import FirebaseAuthService
from controllers.Group import GroupService
from controllers.Movie import MovieService
from controllers.Genre import GenreService
from config.db import session
from controllers.MovieGroupUser import MovieUserGroupService
from controllers.User import UserService
from models.GenreMovie import GenreMovie
from schema.Group import groupSchema
from schema.Movie import MovieResponse

class DataTransfer:

    MovieServiceRepository = MovieService(session)
    GenreServiceRepository = GenreService(session)
    # GroupServiceRepository = GroupService(session,MovieUserGroupService(session))
    # MovieUserGrouServicepRepository = MovieUserGroupService(session)
    # UserServiceRepository = UserService(session,FirebaseAuthService())

    session = session
 
    def get_movie_datatransfer(self,id,language):
        movie = self.MovieServiceRepository.get_movie_id(id)
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
        movies = self.MovieServiceRepository.get_movies(page)
        movies_response = []
        for movie in movies:
            genres_in_movie = session.query(GenreMovie).filter(GenreMovie.id_movie == movie.id).all()
            genres_data = [self.GenreServiceRepository.get_genre(language,genre.id_genre).name for genre in genres_in_movie]
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
                genres = genres_data,
        ))
        return movies_response
    
    def get_group(self,group_id):
        group_data = self.GroupServiceRepository.get_group_id(group_id)
        MovieUserGroupd_Dta = self.MovieUserGrouServicepRepository.get_group_id(group_id)
        user_list = []

        # for group_data_mug in MovieUserGroupd_Dta:
        return ""

        return groupSchema(
                id = group_data.id ,
                owner_id = group_data.owner_id ,
                users = [self.UserServiceRepository.get_user_id(user) for user in MovieUserGroupd_Dta.id_user],
                # movie_toWatch = ,
                # movie_Watched = 
        )

    