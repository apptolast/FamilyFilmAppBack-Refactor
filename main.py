from fastapi import FastAPI
from router import genres, groups, users

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(genres.router)

