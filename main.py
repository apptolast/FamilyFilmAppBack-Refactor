from fastapi import FastAPI
import router
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router=router.users)
app.include_router(router=router.groups)
app.include_router(router=router.genres)
app.include_router(router=router.movies)