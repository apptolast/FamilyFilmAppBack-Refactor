from fastapi import APIRouter,status
from sqlalchemy.exc import IntegrityError
from schema.Movie import MovieCreate
from config.db import session
from models.Movie import Movie



router = APIRouter(
    prefix="/Genre",
    tags=["Genres"]
)



@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_genre(movie: MovieCreate):
    try:
        db_group = Movie(**dict(movie))
        session.add(db_group)
        session.commit()
    except IntegrityError:
        session.rollback()
        return "error"
    session.commit()

    return {"status": "success", "data":Movie(**dict(movie)) }

@router.get('/all')
async def get_movies():
    return session.query(Movie).all()

@router.get('/{id:int}')
async def get_genre(id:int):
        return session.query(Movie).filter(Movie.id == id).first()

@router.patch('/edit/{id:int}')
async def edit_movies(movie:MovieCreate,id:int):
     try:
        session.query(Movie).filter(Movie.id == id).update(dict(movie), synchronize_session=False)
     except IntegrityError:
        session.rollback()
        return 'error'
     session.commit()
     return session.query(Movie).filter(Movie.id == id).first()