from fastapi import APIRouter,status
from sqlalchemy.exc import IntegrityError
from schema.Genre import GenreCreate
from config.db import session
from models.Genre import Genre



router = APIRouter(
    prefix="/Genre",
    tags=["Genres"]
)



@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_genre(genre: GenreCreate):
    try:
        db_group = Genre(name = genre.name)
        session.add(db_group)
    except IntegrityError:
        session.rollback()
        return "error"
    session.commit()
    return genre

@router.get('/all')
async def get_genres():
    return session.query(Genre).all()

@router.get('/{id:int}')
async def get_genre(id:int):
        return session.query(Genre).filter(Genre.id == id).first()

@router.patch('/edit/{id:int}')
async def edit_genre(genre:GenreCreate,id:int):
     try:
        session.query(Genre).filter(Genre.id == id).update(dict(genre), synchronize_session=False)
     except IntegrityError:
        session.rollback()
        return 'error'
     session.commit()
     return session.query(Genre).filter(Genre.id == id).first()
