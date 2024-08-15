import json
import os
from fastapi import HTTPException, Request,status
import requests
from dotenv import load_dotenv
from models.User import User
from controllers.Auth import FirebaseAuthService
from schema.User import UserFirebaseBackendTestRequest, UserSchemaRequest
from models.Language import Language



class UserService:
    
    def __init__(self, db_session, firebase_auth_service):
        self.db_session = db_session
        self.firebase_auth_service = firebase_auth_service
        self.load_dotenv = load_dotenv()

        
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
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user
            
        except HTTPException as http_error:
            raise http_error

        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred:  {str(e)}")
            
    def set_language(self,language,user_id):
        new_language = language.lower()
        
        try:
            if len(new_language) > 2 or len(language) <2:
                raise HTTPException(status_code=404, detail="the language is not possible set in user")

            if self.db_session.query(Language).filter(Language.language == new_language).first() is None:
                set = Language(language = new_language)
                self.db_session.add(set)
                self.db_session.commit()

            id_language = self.db_session.query(Language).filter(Language.language == new_language).first()
            self.get_user_id(user_id).id_language = id_language.id
            self.db_session.commit()
            return self.get_user_id(user_id)
        
        except HTTPException as http_error:
            raise http_error
        
        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred:  {str(e)}")
        
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

    def check_user_exists(self,email):
        try:
            user = self.db_session.query(User).filter(User.email == email).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user
        
        except HTTPException as http_error:
            raise http_error

        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
        
    def create_user_firebase_backend_test(self, user_data: UserFirebaseBackendTestRequest):
        user_record = self.firebase_auth_service.create_firebase_user(
            email=user_data.email,
            password=user_data.password
        )
        custom_token = self.firebase_auth_service.generate_custom_token(user_record.uid)
        custom_token_decoded = custom_token.decode('utf-8')
        return self.id_token_for_backend(custom_token_decoded=custom_token_decoded, user_data=user_data)
            
    def id_token_for_backend(self, custom_token_decoded: str, user_data: UserFirebaseBackendTestRequest):
        url = os.getenv("URL_FOR_BACKEND_TOKEN")
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'token': f"{custom_token_decoded}",
            'returnSecureToken': True
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            self.create_user(user_data=UserSchemaRequest(
                email=user_data.email,
                provider='password'
            ))
            return response.json()
        else:
            return response.status_code, response.text
    
    def id_token_for_login(self, custom_token_decoded: str):
        url = os.getenv("URL_FOR_BACKEND_TOKEN")
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'token': f"{custom_token_decoded}",
            'returnSecureToken': True
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code, response.text
    
    def refresh_automatic_token_logic(self,email: str):
        uid_user = self.firebase_auth_service.get_uid_user(email)
        custom_token = self.firebase_auth_service.generate_custom_token(uid_user)
        custom_token_decoded = custom_token.decode('utf-8')
        return self.id_token_for_login(custom_token_decoded=custom_token_decoded)
    
        
        
    def login_with_custom_token(self, user_data: UserFirebaseBackendTestRequest):
        uid_user = self.firebase_auth_service.get_uid_user(user_data.email)
        custom_token = self.firebase_auth_service.generate_custom_token(uid_user)
        custom_token_decoded = custom_token.decode('utf-8')
        return self.id_token_for_login(custom_token_decoded=custom_token_decoded)
    
    def auth_user(self, request: Request):
        token = request.headers.get("Authorization")
        try:
            token_decoded = self.firebase_auth_service.verify_token(token)
            return token_decoded
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Authentication error: {str(e)}")

