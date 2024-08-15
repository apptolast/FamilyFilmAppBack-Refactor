from datetime import datetime
import logging 
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import Column, Integer,JSON
from config.checkAutomaticTokens import check_token_validation
from config.downloadMoviesAuto import automated_download_movies
from config.firebase import initialize_firebase
from config.logging_config import config_loggin_system
from models.Movie import Movie
from router.users import router as users_router
from router.groups import router as groups_router
from router.genre import router as genres_router
from router.movie import router as movies_router
import os
from config.db import session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os 

load_dotenv()

app = FastAPI()

scheduler = AsyncIOScheduler()
scheduler.start()


config_loggin_system()



logging.info('Inicio del servicio de logging.')



@app.get("/")
async def root():
    
    return {"message": "Hello World Test"}

@app.post("/initgroups")
async def init():
    session.add(Movie(
    id = 0 ,
    title = {"null":"null"},
    synopsis ={"null":"null"},
    image = "null",
    adult =True ,
    release_date = "1977-05-25",
    rating_average =8.203,
    rating_value = 19977
    ))

# Init Firebase Admin SDK and get the app
initialize_firebase()


app.include_router(users_router)
app.include_router(groups_router)
app.include_router(genres_router)
app.include_router(movies_router)

scheduler.add_job(check_token_validation, 'interval', hours=1, next_run_time=datetime.now())
scheduler.add_job(automated_download_movies, 'interval', weeks=1, next_run_time=datetime.now())
