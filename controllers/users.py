from dotenv import load_dotenv
import os
from fastapi import HTTPException, status,Depends
from fastapi.security import OAuth2PasswordBearer
from config.db import session
from models.User import User
from datetime import datetime, timedelta
from schema.Token import Token
from jose import JWTError,jwt
from passlib.context import CryptContext


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(user):
    access_token= {"sub":user.email,
                 "exp":datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))}
    return Token(access_token =  jwt.encode(access_token,SECRET_KEY,algorithm=ALGORITHM),token_type="JWT")


def validate_user(email,password):
    try:
       user = session.query(User).filter(User.email == email).first()
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user incorrected, please try again in a few seconds")
        
    if not (pwd_context.verify(password,user.firebase_uuid)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password incorrected, please try again in a few seconds")
    
    return user

def decode(tk:str):
    try:
        user = jwt.decode(tk,SECRET_KEY,ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401,detail="Credenciales de auth invalidas", headers={"WWW-Authenticate":"Bearer"})
    return user

def search_decode(user):
    try:
        result = session.query(User).filter(User.email == user['sub']).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return result

def auth_user(tk:str = Depends(OAuth2PasswordBearer('/login'))):
    return search_decode(decode(tk))