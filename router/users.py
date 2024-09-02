from typing import List
from fastapi import APIRouter,Depends
from config.readJsonUsers import read_json_users_file
from controllers.DataTransfer import DataTransfer
from schema.User import AutomaticUpdateTokenRequest, AutomaticUpdateTokenResponse, UserFirebaseBackendTestRequest, UserSchemaRequest, UserSchemaResponse, UserTokenResponse
from controllers.User import UserService
from config.db import session
from controllers.Auth import FirebaseAuthService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

firebase_auth_service = FirebaseAuthService()
UserServiceRepository = UserService(session, firebase_auth_service)
returns = DataTransfer()

@router.post('', status_code=201)
async def create_user(me = Depends(UserServiceRepository.auth_user)):
    user = UserSchemaRequest(
        email = me["email"],
        provider = me["firebase"]["sign_in_provider"]
    )
    return UserServiceRepository.create_user(user)
    

@router.post('/backend_test/register', status_code=201, response_model=UserTokenResponse)
async def create_user_firebase_backend_test(user_request: UserFirebaseBackendTestRequest):
    return UserServiceRepository.create_user_firebase_backend_test(user_request)

@router.post('/backend_test/login', status_code=201, response_model=UserTokenResponse)
async def create_user_firebase_backend_test(user_request: UserFirebaseBackendTestRequest):
    return UserServiceRepository.login_with_custom_token(user_request)


@router.post('/automated/token', status_code=200, response_model=UserTokenResponse)
async def get_token(email_request: AutomaticUpdateTokenRequest):
    return UserServiceRepository.refresh_automatic_token_logic(email=email_request.email)

@router.get('', status_code=200)
async def get_users(me = Depends(UserServiceRepository.auth_user)):
    return returns.get_users()

@router.get('/{id:int}',status_code=200)
async def get_user(id:int, me = Depends(UserServiceRepository.auth_user)):
    return returns.get_user_id(id)

@router.get('/me',status_code=200)
async def me(me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.check_user_exists(me['email'])
    return returns.get_user_id(user.id)

@router.delete('',status_code=204)
async def delete_user(me = Depends(UserServiceRepository.delete_user)):
    return get_users()

@router.put('/language/{language}')
async def set_language(language:str ,me = Depends(UserServiceRepository.auth_user)):
    user = UserServiceRepository.get_user_id(user_id= UserServiceRepository.check_user_exists(me['email']).id)
    UserServiceRepository.set_language(user_id=user.id,language= language)
    return returns.get_user_id(user.id)