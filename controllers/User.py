from fastapi import HTTPException, Request,status
from models.User import User
from controllers.Auth import FirebaseAuthService
from schema.User import UserSchemaRequest



class UserService:
    
    def __init__(self, db_session, firebase_auth_service):
        self.db_session = db_session
        self.firebase_auth_service = firebase_auth_service

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


    def delete_user(self, request: Request):
        try:
            user = self.check_user_exists(request=request)
            if user:
                self.firebase_auth_service.delete_user_firebase(email=user.email)
                self.db_session.delete(user)
                self.db_session.commit()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        except HTTPException as http_error:
            raise http_error
        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")


    def check_user_exists_or_create(self, request: Request):
        try:
            decoded_token = self.firebase_auth_service.verify_token(request.headers.get("Authorization"))
            user_email = decoded_token["email"]
            user = self.db_session.query(User).filter(User.email == user_email).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in local database")
            else:
                return user
        except HTTPException as http_error:
            raise http_error
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Check if user exits error: {str(e)}")
    
    
    def create_user(self, user):
        new_user = UserSchemaRequest(
            email=user.email,
            provider=user.provider
        )
        if self.db_session.query(User).filter(User.email == new_user.email).first() is None:
            self.create_user(new_user)
    
    def check_user_exists(self, request: Request):
        try:
            decoded_token = self.firebase_auth_service.verify_token(request.headers.get("Authorization"))
            user_email = decoded_token["email"]
            user = self.db_session.query(User).filter(User.email == user_email).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in local database")
            return user
        except HTTPException as http_error:
            raise http_error
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Check if user exits error: {str(e)}")

    def auth_user(self, request: Request):
        token = request.headers.get("Authorization")
        try:
            # Utiliza la instancia de FirebaseAuthService pasada en el constructor
            token_decoded = self.firebase_auth_service.verify_token(token=token)
            return token_decoded
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Last Step to Auth user error: {str(e)}")

