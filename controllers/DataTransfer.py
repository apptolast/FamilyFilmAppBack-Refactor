from controllers.Auth import FirebaseAuthService
from controllers.Group import GroupService
from controllers.Movie import MovieService
from controllers.Genre import GenreService
from config.db import session
from controllers.MovieGroupUser import MovieUserGroupService
from controllers.User import UserService
from models.GenreMovie import GenreMovie
from models.Group import Group
from models.Language import Language
from schema.Group import groupSchema, usuarito
from schema.Movie import MovieResponse

class DataTransfer:

    MovieServiceRepository = MovieService(session)
    GenreServiceRepository = GenreService(session)
    GroupServiceRepository = GroupService(session,MovieUserGroupService(session))
    MovieUserGrouServicepRepository = MovieUserGroupService(session)
    UserServiceRepository = UserService(session,FirebaseAuthService())

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
        group_name_owner = session.query(Group).filter(Group.id == group_data[0].id_group ).first()
        #     {
        # "id_user": 16,
        # "id_movie": 0,
        # "toWatch": null,
        # "id_group": 3
        #      }

        return groupSchema(
                id = group_data[0].id_group ,
                owner_id = group_name_owner.owner_id,
                name = group_name_owner.name,
                users = [self.get_user_id(user.id_user) for user in group_data]
                # movie_toWatch = ,
                # movie_Watched = 
        )
    
    def get_groups(self,user_id):
        grupos = self.GroupServiceRepository.get_groups(user_id)
        return [self.get_group(grupo.id_group) for grupo in grupos]

    def get_user_id(self,id:int):
        usuario = self.UserServiceRepository.get_user_id(id)
        leng = session.query(Language).filter(Language.id == usuario.id_language).first()
        return usuarito(
            id = usuario.id,
            email=usuario.email,
            language= leng.language,
            provider=usuario.provider
        )
    
    def get_users(self):
        users = self.UserServiceRepository.get_users()
        return [self.get_user_id(user.id) for user in users]
        
    def call_to_update_movies_peer_week(self):
        return self.MovieServiceRepository.update_movies()

    