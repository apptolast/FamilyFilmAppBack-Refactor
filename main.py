from fastapi import FastAPI
from config.firebase import initialize_firebase
from router.genres import router as genres_router
from router.groups import router as groups_router
from router.movies import router as movies_router
from router.users import router as users_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Init Firebase Admin SDK and get the app
initialize_firebase()

app.include_router(genres_router)
app.include_router(groups_router)
app.include_router(movies_router)
app.include_router(users_router)