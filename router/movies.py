from fastapi import APIRouter,status
from controllers.movies import downloadMovie, get_all_movies, get_movie_by_id


router = APIRouter(
    prefix="/Movie",
    tags=["Movies"]
)



@router.post("/create/{lenguage:str}/{page:int}", status_code=status.HTTP_201_CREATED)
async def create_movie(lenguage:str,page:int):
   return downloadMovie(lenguage,page)
 
@router.get('/all/{idiom}/{page}')
async def get_movies(idiom:str,page:int):
    return get_all_movies(idiom,page)

@router.get('/{id:int}/{idiom}')
async def get_movie(id:int,idiom:str):
        return get_movie_by_id(id,idiom)
