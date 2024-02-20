from typing import List
from fastapi import APIRouter
from sqlalchemy import update
from schema.Genre import ShowGenre
from models.Genre import Genre
from controllers.genre import get_all_genres, get_genre_by_id
from controllers.session import add_to_db
from controllers.moviesapi import api,url_genre
from config.db import session



router = APIRouter(
    prefix="/Genre",
    tags=["Genres"]
)

@router.post("/dowloadgenre/{idiom:str}", status_code=201,response_model=List[ShowGenre])
async def create_genre(idiom):

    json_response = api(f'{url_genre}{idiom}')

    for genre in json_response['genres']:
        existing_genre = session.query(Genre).filter(Genre.id == genre['id']).first()
        
        if existing_genre is None:
           add_to_db(Genre(id=genre['id'],name={f"{idiom}":genre['name']}))
        else:
            existing_genre.name = {**existing_genre.name, idiom: genre['name']}
            session.commit()
        
    
    return get_all_genres(idiom)

@router.get('/all/{idiom:str}',status_code=200, response_model=List[ShowGenre])
async def get_genres(idiom:str):
    return get_all_genres(idiom)

@router.get('/{id:int}/{idiom:str}',status_code=200, response_model=ShowGenre)
async def get_genre(id:int,idiom):
        return get_genre_by_id(id,idiom)

