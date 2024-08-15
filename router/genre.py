from fastapi import APIRouter, Depends, HTTPException
from config.db import session
from controllers.Genre import GenreService
from controllers.DataTransfer import DataTransfer
from router.users import UserServiceRepository

router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)

GenreServiceRepository = GenreService(session)
returns = DataTransfer()

@router.post("")
async def dowload_genres(me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    return GenreServiceRepository.dowload_genres(returns.get_user_id(user.id).language)

@router.get("/{idiom}")
async def get_genres(idiom:str,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)

    return GenreServiceRepository.get_genres(idiom)


