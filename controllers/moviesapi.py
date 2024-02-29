import requests
from dotenv import load_dotenv
import os 

load_dotenv()

url_genre= "https://api.themoviedb.org/3/genre/movie/list?language="

adult = False
video = False
language = 'en'

# Define la base de la URL sin el parámetro de página
base_url_movies = f"https://api.themoviedb.org/3/discover/movie?include_adult={adult}&include_video={video}&language={language}&sort_by=popularity.desc"


def api(url):
    return requests.get(url, headers={
        "accept": "application/json",
        "Authorization": os.getenv('header_authorization')
    }).json()