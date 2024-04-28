from fastapi import Request, HTTPException, status
from firebase_admin import auth

async def firebase_auth_middleware(request: Request, call_next):
    # Lista de rutas que no requieren autenticación
    path_check = request.url.path.endswith
    if not (path_check("/user/login") or path_check("/user/create")):
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token is missing")
        try:
            # Extrae el token Bearer
            token = token.replace("Bearer ", "")
            decoded_token = auth.verify_id_token(token)
            request.state.user = decoded_token
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

    response = await call_next(request)
    return response
