from fastapi import HTTPException, Request,status
from models.User import User
from firebase_admin import auth as firebase_auth
from schema.User import UserSchemaRequest
from firebase_admin import auth

class UserService:
    
    def __init__(self, db_session):
        self.db_session = db_session

    def create_user(self, user):
            new_user = User(
                 email = user.email,
                 provider = user.provider
            )
            try:
                self.db_session.add(new_user)
                self.db_session.commit()
                
            except Exception as e:
                 self.db_session.rollback()
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
            
            return self.db_session.query(User).filter(User.email == new_user.email).first()
        
    def get_users(self):
        try:
            user = self.db_session.query(User).all()
            return user
        except Exception as e:
             self.db_session.rollback()
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"No existen usuarios")

    
    def get_user_id(self, user_id):
        try:
            user = self.db_session.query(User).filter(User.id == user_id).first()
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
            
        except HTTPException as http_error:
            raise http_error

        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred:  {str(e)}")
            


    # def update_user(self,user):
    #     user = self.get_user_by_id(user.id)
    #     if user:
    #         for key, value in kwargs.items():
    #             setattr(user, key, value)
    #         self.db_session.commit()
    #         return user

    def delete_user(self, user):
        try:    
            if user :
                current_user = auth.get_user_by_email(user.email) 
                auth.delete_user(current_user.uid)
                self.db_session.delete(user)
                self.db_session.commit()
            return True
        
        except Exception as e: 
            self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred:  {str(e)}")

            


    
    def auth_user(self,request: Request):
        token = request.headers.get("Authorization")
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        try:
            if token.startswith("Bearer "):
                token = token[7:]
            decoded_token = firebase_auth.verify_id_token(token)
            new_user = UserSchemaRequest(
                email=decoded_token["email"],
                provider=decoded_token["firebase"]["sign_in_provider"])
            if self.db_session.query(User).filter(User.email == new_user.email).first() is None:
                self.create_user(new_user)
            return self.db_session.query(User).filter(User.email == new_user.email).first()
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid authentication credentials: {str(e)}")
        

