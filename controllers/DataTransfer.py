import logging
import random
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
from schema.Group import MovieGroup, groupSchema, usuarito
from schema.Movie import MovieResponse
from fastapi import HTTPException,status

class DataTransfer:

    MovieServiceRepository = MovieService(session)
    GenreServiceRepository = GenreService(session)
    GroupServiceRepository = GroupService(session,MovieUserGroupService(session))
    MovieUserGrouServiceRepository = MovieUserGroupService(session)
    UserServiceRepository = UserService(session,FirebaseAuthService())

    session = session


    def get_recomendation_movie(self,id_group):
        users = self.get_group(id_group,"es").users

        users_en = sum(1
                        for user in users
                        if user.language == "en")
        
        recommended_language = "en" if users_en >= (len(users) - users_en) else "es"
        movies = self.get_group(id_group,recommended_language).to_Watch

        if len(movies) > 0:
            return random.choice(movies)
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found, please add movies")
        

    def get_movie_datatransfer(self, id: int, language: str):
        # Obtener la película desde el repositorio
        movie = self.MovieServiceRepository.get_movie_id(id)
        
        # Verificar si la película existe
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        
        # Obtener los géneros asociados con la película
        genres_in_movie = session.query(GenreMovie).filter(GenreMovie.id_movie == movie.id).all()
        genres_name = [self.GenreServiceRepository.get_genre(language, genre.id_genre).name for genre in genres_in_movie]
        
        # Verificar que el título y la sinopsis existen en el idioma solicitado
        if not movie.title.get(language) or not movie.synopsis.get(language):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found in the specified language")
        
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

    
    def get_movies_datatransfer(self, language, page, page_size=20):
        movies_response = []

        while len(movies_response) < page_size:
                movies = self.MovieServiceRepository.get_movies(page,language)

                if not movies:
                    break

                for movie in movies:
                    # Verificar si la película tiene datos en el idioma solicitado
                    if language in movie.title and language in movie.synopsis:
                        # Obtener géneros de la película en el idioma solicitado
                        genres_in_movie = session.query(GenreMovie).filter(GenreMovie.id_movie == movie.id).all()
                        genres_data = [
                            self.GenreServiceRepository.get_genre(language, genre.id_genre).name
                            for genre in genres_in_movie
                        ]
                        # Crear la respuesta de la película con los datos en el idioma solicitado
                        movies_response.append(
                            MovieResponse(
                                id=movie.id,
                                title=movie.title[language],
                                synopsis=movie.synopsis[language],
                                image=movie.image,
                                adult=movie.adult,
                                release_date=movie.release_date,
                                rating_average=movie.rating_average,
                                rating_value=movie.rating_value,
                                genres=genres_data,
                             )
                        )

                page =+1

        return movies_response[:page_size]
    
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
                movie = self.MovieServiceRepository.get_movie_or_none(group.id_movie,language)
                if movie is None:
                    continue
                if group.toWatch == True and group.id_movie != 0:
                    movies_to_watched.append(movie)
                if group.toWatch == False and group.id_movie != 0:
                    movies_to_watch.append(movie)

        return groupSchema(
                id = group_data[0].id_group ,
                owner_id = group_name_owner.owner_id,
                name = group_name_owner.name,
                users = self.not_duplicated_users(group_data),
                watch= movies_to_watch,
                watched=movies_to_watched
        )
    
    def get_all_groups_for_user(self,user_id,language):
        created_groups = self.GroupServiceRepository.get_groups(user_id)
        member_groups = self.GroupServiceRepository.get_member_groups(user_id)
        all_groups = created_groups + member_groups
        return self.not_duplicated_groups(all_groups,language)
    
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

    # def get_user_id(self,id:int):
    #     usuario = self.UserServiceRepository.get_user_id(id)
         
    #     try:
    #         leng = session.query(Language).filter(Language.id == usuario.id_language).first()         
    #         if leng is not None:
    #             leng = leng.language

    #         return usuarito(
    #             id = usuario.id,
    #             email=usuario.email,
    #             language= leng,
    #             provider=usuario.provider
    #         )
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"{str(e)}")
        
    def get_user_id(self,id:int):
        usuario = self.UserServiceRepository.get_user_id(id)
        movies = self.MovieUserGrouServiceRepository.get_groups(id)
         
        try:
            leng = session.query(Language).filter(Language.id == usuario.id_language).first()         
            if leng is not None:
                leng = leng.language

            movies_watch = []
            movies_watched = []

            for movie in movies:
                
                if movie.toWatch == False:
                    movies_watched.append(
                        MovieGroup(
                            id_group=movie.id_group,
                            id_movie=movie.id_movie
                        ) 
                    )
                else:
                    movies_watch.append(
                        MovieGroup(
                            id_group=movie.id_group,
                            id_movie=movie.id_movie
                        ) 
                    )

            return usuarito(
                id = usuario.id,
                email=usuario.email,
                language= leng,
                provider=usuario.provider,
                movies_watch=movies_watch,
                movies_watched=movies_watched
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{str(e)}")
    
    def get_users(self):
        users = self.UserServiceRepository.get_users()
        return [self.get_user_id(user.id) for user in users]
        
    def call_to_update_movies_peer_week(self, genre_service: GenreService):
        return self.MovieServiceRepository.update_movies(genre_service=genre_service)
    
    def get_movies_datatransfer_by_name(self, language, page, name, page_size=20):
        movies_response = []
        
        while len(movies_response) < page_size:
                movies = self.MovieServiceRepository.get_movie_name(language,name,page)

                if not movies:
                    break

                for movie in movies:
                    # Verificar si la película tiene datos en el idioma solicitado
                    if language in movie.title and language in movie.synopsis:
                        # Obtener géneros de la película en el idioma solicitado
                        genres_in_movie = session.query(GenreMovie).filter(GenreMovie.id_movie == movie.id).all()
                        genres_data = [
                            self.GenreServiceRepository.get_genre(language, genre.id_genre).name
                            for genre in genres_in_movie
                        ]
                        # Crear la respuesta de la película con los datos en el idioma solicitado
                        movies_response.append(
                            {
                            "id":movie.id,
                            "title":movie.title[language],
                            "synopsis":movie.synopsis[language],
                            "image":movie.image,
                            "adult":movie.adult,
                            "release_date":movie.release_date,
                            "rating_average":movie.rating_average,
                            "rating_value":movie.rating_value,
                            "genres":genres_data
                            }
                        )
                        

                page =+1

        return movies_response[:page_size]
    