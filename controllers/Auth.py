from fastapi import HTTPException, status
from firebase_admin import auth as firebase_auth


class FirebaseAuthService:


    def create_firebase_user(self, email: str, password: str):
        try:
            user_record = firebase_auth.create_user(
                email=email,
                email_verified=True,
                password=password,
            )
            return user_record
        except firebase_auth.FirebaseError as e:
            raise HTTPException(status_code=400, detail=f"Firebase error: {str(e)}")

    def generate_custom_token(self, uid: str):
        try:
            custom_token = firebase_auth.create_custom_token(uid)
            return custom_token
        except firebase_auth.FirebaseError as e:
            raise HTTPException(status_code=400, detail=f"Failed to create custom token: {str(e)}")

    def verify_token(self, token: str):
        try:
            if not token.startswith("Bearer ") or len(token) < 8 or len(token) > 2048 or token[7:] == "" or token == "" or token is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid format token must start with 'Bearer '")
            decoded_token = firebase_auth.verify_id_token(token[7:])
            return decoded_token
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Error when verify with Firebase: {str(e)}")
            
    def delete_user_firebase(self,email:str):
        try:
            current_user = firebase_auth.get_user_by_email(email)
            firebase_auth.delete_user(current_user.uid)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"An error occurred while delete user from Firebase: {str(e)}")