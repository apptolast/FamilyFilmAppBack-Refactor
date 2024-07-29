import logging
from fastapi import APIRouter, Depends, HTTPException
from config.db import session
from controllers.Movie import MovieService
from controllers.DataTransfer import DataTransfer
from router.users import UserServiceRepository
from schema.Movie import AutomaticResponseForMovies
from schema.MovieUserGroup import MovieSearchName

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

MovieServiceRepository = MovieService(session)

returns = DataTransfer()
@router.get("/catalogue/{page}")
async def get_movies(page:int,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    MovieServiceRepository.download_movie(returns.get_user_id(user.id).language,page)
    return returns.get_movies_datatransfer(returns.get_user_id(user.id).language,page)


@router.get("/{id}")
async def get_movie_id(id:int,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return returns.get_movie_datatransfer(id,returns.get_user_id(user.id).language)

@router.get("name/{page}")
async def get_movie_name(Movie_name:MovieSearchName,page:int,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    MovieServiceRepository.download_movie_by_name(returns.get_user_id(user.id).language,Movie_name,page)
    return [ returns.get_movie_datatransfer(movie['id'],returns.get_user_id(user.id).language) for movie in MovieServiceRepository.download_movie_by_name(returns.get_user_id(user.id).language,Movie_name,page)]

# @router.get('/update/movies/automated', status_code=200, response_model=AutomaticResponseForMovies)
# async def updated_movies_endpoint():
#     try:
#         response = DataTransfer().call_to_update_movies_peer_week(genre_service=DataTransfer().GenreServiceRepository)
#         return response
#     except Exception as e:
#         logging.error(f"Error updating movies: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
