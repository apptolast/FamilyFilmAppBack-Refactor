from fastapi import HTTPException, status
from firebase_admin import auth as firebase_auth


class FirebaseAuthService:

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