import requests
from dotenv import load_dotenv
import os 

load_dotenv()

url_genre="https://api.themoviedb.org/3/genre/movie/list?language="

def api(url):
    return requests.get(url, headers={
        "accept": "application/json",
        "Authorization": os.getenv('header_authorization')
    }).json()