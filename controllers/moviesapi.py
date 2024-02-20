import requests
from dotenv import load_dotenv
import os 

load_dotenv()

url_genre= "https://api.themoviedb.org/3/genre/movie/list?language="

adult =False
video = False
lenguage = 'en'
page = 1

url_movies =f"https://api.themoviedb.org/3/discover/movie?include_adult={adult}&include_video={video}&language={lenguage}&page={page}&sort_by=popularity.desc"



def api(url):
    return requests.get(url, headers={
        "accept": "application/json",
        "Authorization": os.getenv('header_authorization')
    }).json()


    #   "id": 787699,
    #   "adult": false,
    #   "genre_ids": [
    #     35,
    #     10751,
    #     14
    #   ],
    #   "original_title": "Wonka",
    #   "original_language": "en",
    #   "overview": "Basada en el personaje que protagoniza \"Charlie y la fábrica de chocolate\", el libro infantil más emblemático de Roald Dahl y uno de los más vendidos de todos los tiempos, \"Wonka\" cuenta la historia de cómo el mayor inventor, mago y chocolatero del mundo se convirtió en el querido Willy Wonka que conocemos hoy en día.",
    #   "popularity": 1523.973,
    #   "poster_path": "/tFyQa5WQqldIL44HBLaCmn5eERD.jpg",
    #   "release_date": "2023-12-06",
    #   "vote_average": 7.202,
    #   "vote_count": 2180
    # },