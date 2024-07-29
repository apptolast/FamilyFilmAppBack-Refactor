import logging
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
from fastapi import HTTPException

class DataTransfer:

    MovieServiceRepository = MovieService(session)
    GenreServiceRepository = GenreService(session)
    GroupServiceRepository = GroupService(session,MovieUserGroupService(session))
    MovieUserGrouServiceRepository = MovieUserGroupService(session)
    UserServiceRepository = UserService(session,FirebaseAuthService())

    session = session
 
    def get_movie_datatransfer(self,id,language):
        movie = self.MovieServiceRepository.get_movie_id(id)
        genres_in_movie = session.query(GenreMovie).filter(GenreMovie.id_movie == movie.id).all()
        genres_name = [self.GenreServiceRepository.get_genre(language,genre.id_genre).name for genre in genres_in_movie]
        
        return movie
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
        )
    
    def get_movies_datatransfer(self,language,page):
        movies = self.MovieServiceRepository.get_movies(page)
        movies_response = []
        for movie in movies:
            print(movie)
            genres_in_movie = session.query(GenreMovie).filter(GenreMovie.id_movie == movie.id).all()
            genres_data = [self.GenreServiceRepository.get_genre(language,genre.id_genre).name for genre in genres_in_movie]
            movies_response.append(
        #         MovieResponse(
        #         id = movie.id,
        #         synopsis = movie.synopsis[language],
        #         title = movie.title[language],
        #         image = movie.image,
        #         adult = movie.adult,
        #         release_date = movie.release_date,
        #         rating_value = movie.rating_value,
        #         rating_average = movie.rating_average,
        #         genres = genres_data
        # ))
            movie
            )
        return movies
    
    def get_group(self,group_id, language):
        group_data = self.GroupServiceRepository.get_group_id(group_id)
        group_name_owner = session.query(Group).filter(Group.id == group_data[0].id_group).first()
        #     {
        # "id_user": 16,
        # "id_movie": 0,
        # "toWatch": null,
        # "id_group": 3
        #      }
        movies_to_watch = []
        movies_to_watched = []
        if len(group_data) > 0:
            for group in group_data:
                if group.toWatch == True and group.id_movie != 0:
                    print(self.get_movie_datatransfer(group.id_movie,language))
                    movies_to_watched.append(self.get_movie_datatransfer(group.id_movie,language))
                if group.toWatch == False and group.id_movie != 0:
                    print(self.get_movie_datatransfer(group.id_movie,language))
                    movies_to_watch.append(self.get_movie_datatransfer(group.id_movie,language))

        return groupSchema(
                id = group_data[0].id_group ,
                owner_id = group_name_owner.owner_id,
                name = group_name_owner.name,
                users = self.not_duplicated_users(group_data),
                to_Watch= movies_to_watch,
                to_Watched=movies_to_watched
        )
    
    def not_duplicated_users(self,group_data):
        users_id = set()
        for user in group_data:
            if user.id_user not in users_id:
                users_id.add(user.id_user)
        return [self.get_user_id(id) for id in users_id]

    def get_groups(self,user_id,language):
        grupos = self.GroupServiceRepository.get_groups(user_id)
        return self.not_duplicated_groups(groups=grupos,language=language)

    def not_duplicated_groups(self,groups,language):
        groups_id = set()
        for group in groups:
            if group.id_group not in groups_id:
                groups_id.add(group.id_group)
        return [self.get_group(id,language) for id in groups_id]

    def get_user_id(self,id:int):
        usuario = self.UserServiceRepository.get_user_id(id)
        try:
            leng = session.query(Language).filter(Language.id == usuario.id_language).first()         
            if leng is not None:
                leng = leng.language
            return usuarito(
                id = usuario.id,
                email=usuario.email,
                language= leng,
                provider=usuario.provider
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{str(e)}")
    
    def get_users(self):
        users = self.UserServiceRepository.get_users()
        return [self.get_user_id(user.id) for user in users]
        
    def call_to_update_movies_peer_week(self, genre_service: GenreService):
        return self.MovieServiceRepository.update_movies(genre_service=genre_service)
    
    def add_to_watch(self,user_id,group_id,movie_id,language):
        self.GroupServiceRepository.add_to_watch(user_id,group_id,movie_id)


    