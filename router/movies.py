from fastapi import APIRouter,status
from schema.Movie import MovieCreate
from config.db import session
from models.Movie import Movie
from controllers.session import add_to_db
from controllers.moviesapi import url_movies,api
from controllers.movies import downloadMovie


router = APIRouter(
    prefix="/Movie",
    tags=["Movies"]
)



@router.post("/create/{lenguage:str}", status_code=status.HTTP_201_CREATED)
async def create_genre(lenguage:str):
   return downloadMovie(lenguage)
 
        
    
    


@router.get('/all')
async def get_movies():
    return session.query(Movie).all()

@router.get('/{id:int}')
async def get_genre(id:int):
        return session.query(Movie).filter(Movie.id == id).first()





    # {
    #   "adult": false,
    #   "backdrop_path": "/yyFc8Iclt2jxPmLztbP617xXllT.jpg",
    #   "genre_ids": [
    #     35,
    #     10751,
    #     14
    #   ],
    #   "id": 787699,
    #   "original_language": "en",
    #   "original_title": "Wonka",
    #   "overview": "Basada en el personaje que protagoniza \"Charlie y la fábrica de chocolate\", el libro infantil más emblemático de Roald Dahl y uno de los más vendidos de todos los tiempos, \"Wonka\" cuenta la historia de cómo el mayor inventor, mago y chocolatero del mundo se convirtió en el querido Willy Wonka que conocemos hoy en día.",
    #   "popularity": 1523.973,
    #   "poster_path": "/tFyQa5WQqldIL44HBLaCmn5eERD.jpg",
    #   "release_date": "2023-12-06",
    #   "title": "Wonka",
    #   "video": false,
    #   "vote_average": 7.202,
    #   "vote_count": 2180
    # },