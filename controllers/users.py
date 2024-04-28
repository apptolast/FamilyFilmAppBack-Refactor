from dotenv import load_dotenv
import os
from fastapi import HTTPException, Request, status
from config.db import session
from controllers.session import check_column
from models.Group import Group
from models.GroupUser import GroupUser
from models.User import User
from datetime import datetime, timedelta
import schema
from schema.Token import Token 
from jose import jwt
from passlib.context import CryptContext
from firebase_admin import auth as firebase_auth

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(user):
    access_token= {"sub":user.email,
                 "exp":datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))}
    return Token(access_token =  jwt.encode(access_token,SECRET_KEY,algorithm=ALGORITHM),token_type="JWT")



def auth_user(request: Request):
    #Extract token from header
    token = request.headers.get("Authorization")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        # Remover el prefijo "Bearer" si está presente
        if token.startswith("Bearer "):
            token = token[7:]
        # Verificar el token con Firebase Admin SDK
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


def get_all_users():
    try:
        users = session.query(User).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return users

def filter_user(user_colum,user_data):
    try:
        check_column(user_colum,User)
        user = session.query(User).filter(getattr(User, user_colum) == user_data).first()
        is_user(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return user

def is_user(user):
     if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

def create_userdata(user):
    all_groups = session.query(Group).all()

    group_owners = [session.query(GroupUser).filter(GroupUser.group_id == group.id).order_by(GroupUser.group_id).first() for group in all_groups]

    owned_groups = [group for group, owner in zip(all_groups, group_owners) if owner.user_id == user.id]

    groups_id = [group.id for group in owned_groups]

    return schema.User.UserData(
        userId=user.id,
        groupId=groups_id,
        user={"userId": user.id,"email": user.email,"provider":"","role": user.role}
    )
 