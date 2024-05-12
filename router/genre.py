from fastapi import APIRouter
from config.db import session
from controllers.Genre import GenreService


router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)

GenreServiceRepository = GenreService(session)

@router.get("/{idiom}")
async def get_genres(idiom:str):
    return GenreServiceRepository.get_genres(idiom)


