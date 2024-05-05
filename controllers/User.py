from fastapi import HTTPException, Request,status
from models.User import User
from firebase_admin import auth as firebase_auth
from config.db import session
from schema.User import UserSchemaRequest

class UserService:
    
    
    def __init__(self, db_session=session):
            self.db_session = db_session

    def create_user(self, user):
            new_user = User(user)
            self.db_session.add(new_user)
            self.db_session.commit()
            return new_user
        
    def get_users(self):
        return self.db_session.query(User).all()
    
    # def get_user_id(self, user_id):
    #     return self.db_session.query(User).filter(User.id == user_id).first()

    # def update_user(self, user_id, **kwargs):
    #     user = self.get_user_by_id(user_id)
    #     if user:
    #         for key, value in kwargs.items():
    #             setattr(user, key, value)
    #         self.db_session.commit()
    #         return user

    # def delete_user(self, user_id):
    #     user = self.get_user_by_id(user_id)
        
    #     if user:
    #         self.db_session.delete(user)
    #         self.db_session.commit()
        
    #     return False

    
    def auth_user(self,request: Request):
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

            new_user = UserSchemaRequest(
                email=decoded_token["email"],
                provider=decoded_token["firebase"]["sign_in_provider"])
            
            if self.db_session.query(User).filter(User.email == new_user.email).first() is None:
                self.create_user(new_user)
            
            return self.db_session.query(User).filter(User.email == new_user.email).first()
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"el error es: {e}")