from fastapi import HTTPException, status
from firebase_admin import auth as firebase_auth


class FirebaseAuthService:
    def verify_token(self, token: str):
        try:
            if not token.startswith("Bearer "):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            decoded_token = firebase_auth.verify_id_token(token[7:])
            return decoded_token
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid authentication credentials: {str(e)}")