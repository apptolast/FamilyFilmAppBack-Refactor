import logging
from fastapi import APIRouter, HTTPException
from config.db import session
from controllers.Movie import MovieService
from controllers.DataTransfer import DataTransfer
from schema.Movie import AutomaticResponseForMovies

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

MovieServiceRepository = MovieService(session)

@router.get("/{page}/{leng}")
async def get_movies(page:int,leng:str):
    return DataTransfer().get_movies_datatransfer(leng,page)

@router.get("/{id}")
async def get_movies(id:int):
    return DataTransfer().get_movie_datatransfer(id,'es')

@router.get('/update/movies/automated', status_code=200, response_model=AutomaticResponseForMovies)
async def updated_movies_endpoint():
    try:
        response = DataTransfer().call_to_update_movies_peer_week(genre_service=DataTransfer().GenreServiceRepository)
        return response
    except Exception as e:
        logging.error(f"Error updating movies: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")