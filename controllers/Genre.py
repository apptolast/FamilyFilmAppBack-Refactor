import os
from fastapi import HTTPException
import requests
from sqlalchemy import func, text
from models import Genre
from schema.Genre import GenreResponse


class GenreService:

    url_genre= "https://api.themoviedb.org/3/genre/movie/list?language="

    def __init__(self,db_session):
        self.db_session = db_session


    def get_genre(self,language,id):
        self.check_genres_downloads(language)
        genre = self.db_session.query(Genre.id, text(f"genres.name->>'{language}'")).filter(Genre.id == id).first()
        return GenreResponse(id = genre[0], name = genre[1])

    def get_genres(self,language):
        self.check_genres_downloads(language)
        genres = self.db_session.query(Genre.id, text(f"genres.name->>'{language}'")).all()
        return [GenreResponse(id = genre[0], name = genre[1])for genre in genres]

    def check_genres_downloads(self,language):
        if len(self.db_session.query(Genre.id, text(f"genres.name->>'{language}'")).all()) <= 0:
            self.dowload_genres(language)
            self.check_genres_downloads(language)
    
    def dowload_genres(self,language):

        json_response = GenreService.api_start(f'{self.url_genre}{language}')

        for genre in json_response['genres']:
            existing_genre = self.db_session.query(Genre).filter(Genre.id == genre['id']).first()
            
            if existing_genre is None:
                self.db_session.add(Genre(id=genre['id'],name={f"{language}":genre['name']}))
            else:
                existing_genre.name = {**existing_genre.name, language: genre['name']}
                self.db_session.commit()
    
    @staticmethod
    def api_start(url):
        return requests.get(url, headers={
            "accept": "application/json",
            "Authorization": os.getenv('header_authorization')
        }).json()

    


        
    

        
