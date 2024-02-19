from fastapi import APIRouter,status
from sqlalchemy.exc import IntegrityError
from schema.Genre import GenreCreate
from config.db import session
from models.Genre import Genre
from controllers.genre import genre_filter, get_all_genres, get_genre_by_id
from controllers.session import add_to_db
from controllers.moviesapi import api,url_genre
from googletrans import Translator, constants
from pprint import pprint

translator = Translator()

router = APIRouter(
    prefix="/Genre",
    tags=["Genres"]
)

@router.post("/dowloadgenre/{idiom:str}", status_code=status.HTTP_201_CREATED)
async def create_genre(idiom):
    json_response = api(f'{url_genre}{idiom}')

    for genre in json_response['genres']:
        if genre_filter(idiom,genre['name']) == None:
           add_to_db(Genre(id=genre['id'],name={f"{idiom}":genre['name']}))
    
    return get_all_genres()

@router.get('/all/{idiom:str}')
async def get_genres(idiom:str):
    return get_all_genres(idiom)

@router.get('/{id:int}/{idiom:str}')
async def get_genre(id:int):
        return get_genre_by_id(id)

