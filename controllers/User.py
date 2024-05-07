from fastapi import HTTPException, Request,status
from models.User import User
from controllers.Auth import FirebaseAuthService
from schema.User import UserSchemaRequest



class UserService:
    
    def __init__(self, db_session, firebase_auth_service):
        self.db_session = db_session
        self.firebase_auth_service = firebase_auth_service

        
    def get_users(self):
        try:
            user = self.db_session.query(User).all()
            return user
        except Exception as e:
             self.db_session.rollback()
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"No existen usuarios {e}")

    
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
            user = self.check_user_exists_or_create(request=request)
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


    def create_user(self, user_data):
        new_user = User(
            email=user_data.email,
            provider=user_data.provider
        )
        try:
            self.db_session.add(new_user)
            self.db_session.commit()
            return new_user
        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def check_user_exists_or_create(self, request: Request):
        decoded_token = self.auth_user(request=request.headers.get("Authorization"))
        user_email = decoded_token["email"]
        user_provider = decoded_token["firebase"]["sign_in_provider"]
        user = self.db_session.query(User).filter(User.email == user_email).first()
        if user is None:
            user_schema = UserSchemaRequest(email=user_email, provider=user_provider)
            user = self.create_user(user_data=user_schema)
        return user
        
        
    def create_user_firebase_backend_test(self, user_data: UserSchemaRequest):
        # Crea usuario en Firebase
        user_record = self.firebase_auth_service.create_firebase_user(
            email=user_data.email,
            password="secretPassword",  # Suponer una contraseña predeterminada o solicitarla
            phone_number="+15555550100",  # Suponer o solicitar
            display_name=user_data.display_name if hasattr(user_data, 'display_name') else '',
            photo_url="http://www.example.com/12345678/photo.png",  # Suponer o solicitar
            disabled=False
        )
        # Generar token personalizado para el usuario
        custom_token = self.firebase_auth_service.generate_custom_token(user_record.uid)

        # Crear usuario en la base de datos local si es necesario
        existing_user = self.db_session.query(User).filter_by(email=user_data.email).first()
        if not existing_user:
            new_user = User(email=user_data.email, provider='firebase')
            self.db_session.add(new_user)
            self.db_session.commit()

        return {"user": user_record, "token": custom_token}
        
    def auth_user(self, request: Request):
        token = request.headers.get("Authorization")
        try:
            token_decoded = self.firebase_auth_service.verify_token(token)
            return token_decoded
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Authentication error: {str(e)}")
