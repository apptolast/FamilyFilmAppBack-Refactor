from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordBearer
import sqlalchemy.exc
from config.db import session
from controllers.users import auth_user, create_token, validate_user
from schema.User import userCreate,userLogin
from models.User import User



router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post('/create')
async def create_user(user:userCreate):
    try:
        session.add(User(**dict(user)))
        session.commit()
        session.close()
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        return 'error'
    return userLogin(**dict(user))


@router.get('/all')
async def get_users():
    return session.query(User).all()

@router.get('/{id:int}')
async def get_user(id:int):
        return  session.query(User).filter(User.id == id).first()

oauth = OAuth2PasswordBearer(tokenUrl="/login")
@router.post('/login')
async def login_user(user:userLogin):
     user_validate = validate_user(user.email,user.firebase_uuid)
     return create_token(user_validate)


@router.get('/me')
async def me(user = Depends(auth_user)):
    return user