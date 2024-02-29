from fastapi import APIRouter,status
from controllers.movies import downloadMovie, get_all_movies, get_movie_by_id


router = APIRouter(
    prefix="/Movie",
    tags=["Movies"]
)



@router.post("/create/{lenguage:str}", status_code=status.HTTP_201_CREATED)
async def create_genre(lenguage:str):
   return downloadMovie(lenguage)
 
        
    
@router.get('/all/{idiom}')
async def get_movies(idiom:str):
    return get_all_movies(idiom)

@router.get('/{id:int}')
async def get_movie(id:int):
        return get_movie_by_id(id)
