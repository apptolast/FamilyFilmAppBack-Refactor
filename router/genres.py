from fastapi import APIRouter,status
from sqlalchemy.exc import IntegrityError
from schema.Genre import GenreCreate
from config.db import session
from models.Genre import Genre
from controllers.genre import genre_filter, get_all_genres, get_genre_by_id
from controllers.session import add_to_db
from controllers.moviesapi import api,url_genre

router = APIRouter(
    prefix="/Genre",
    tags=["Genres"]
)

@router.post("/dowloadgenre", status_code=status.HTTP_201_CREATED)
async def create_genre():
    json_response = api(url_genre)

    for genre in json_response['genres']:
        if genre_filter(genre['name']) == None:
            add_to_db(Genre(id=genre['id'], name=genre['name']))

    return get_all_genres()

@router.get('/all')
async def get_genres():
    return get_all_genres()

@router.get('/{id:int}')
async def get_genre(id:int):
        return get_genre_by_id(id)
