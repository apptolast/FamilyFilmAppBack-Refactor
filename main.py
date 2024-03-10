from fastapi import FastAPI
from .router import genres_router, groups_router, movies_router, users_router
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(genres_router)
app.include_router(groups_router)
app.include_router(movies_router)
app.include_router(users_router)