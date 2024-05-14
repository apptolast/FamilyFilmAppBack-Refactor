from fastapi import APIRouter
from config.db import session
from controllers.Movie import MovieService
from controllers.DataTransfer import DataTransfer

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

@router.get('/update/movies/automated')
async def updated_movies_endpoint():
    return DataTransfer().call_to_update_movies_peer_week()