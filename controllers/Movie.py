import os
from fastapi import HTTPException,status
import requests
from models.GenreMovie import GenreMovie
from models.Movie import Movie
from models.Language import Language
from sqlalchemy import func, text

class MovieService:

    def __init__(self,db_session):
        self.db_session = db_session
    
    def get_movies(self,page):
        
        items_per_page = 20
        start = (page - 1) * items_per_page
        end = start + items_per_page

        try:
            movies = self.db_session.query(Movie).slice(start, end).all()
            return movies
        except Exception as e:
             self.db_session.rollback()
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"No existen usuarios {e}")

    def get_movie_id(self,movie_id):
        try:
            movie = self.db_session.query(Movie).filter(Movie.id == movie_id).first()
            if not movie:
                raise HTTPException(status_code=404, detail="Movie not found")
            return movie
            
        except HTTPException as http_error:
            raise http_error

        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred:  {str(e)}")
    
    def download_movie(self, language, page, adult=True, video=True):
        print(f"EL LENGUAJE EN LA FUNCION DOWNLOAD ES {language}")

        if page > 500:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The page limit is 500")

        movie_downloads = []
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult={adult}&include_video={video}&language={language}&sort_by=popularity.desc&page={page}"
        print(f"Request URL: {url}")

        # Fetch the movies
        response = self.api_start(url)
        movies = response.get('results', [])
        print(f"Movies fetched: {len(movies)}")

        for movie in movies:
            existing_movie = self.db_session.query(Movie).filter(Movie.id == movie['id']).first()
            print(f"Checking movie: {movie['id']}")
            movie_downloads.append(new_movie)

            if existing_movie is None:
                # Add new movie if it doesn't exist
                print(f"Adding new movie: {movie['title']}")
                new_movie = Movie(
                    id=movie['id'],
                    title={language: movie['title']},
                    synopsis={language: movie['overview']},
                    image=movie['poster_path'],
                    adult=movie['adult'],
                    release_date=movie['release_date'],
                    rating_average=movie['vote_average'],
                    rating_value=movie['vote_count']
                )
                self.db_session.add(new_movie)

                # Commit all changes once after all movies are processed
                try:
                    self.db_session.commit()
                    print("All changes committed successfully.")
                except Exception as e:
                    self.db_session.rollback()
                    print(f"Error committing changes: {e}")

            else:
                # Update existing movie's title and synopsis
                title_data = existing_movie.title if isinstance(existing_movie.title, dict) else {}
                synopsis_data = existing_movie.synopsis if isinstance(existing_movie.synopsis, dict) else {}

                title_data[language] = movie['title']
                synopsis_data[language] = movie['overview']

                existing_movie.title = title_data
                existing_movie.synopsis = synopsis_data

                print(f"Updated title: {existing_movie.title}")
                print(f"Updated synopsis: {existing_movie.synopsis}")

                try:
                    self.db_session.commit()
                    print("All changes committed successfully.")
                except Exception as e:
                    self.db_session.rollback()
                    print(f"Error committing changes: {e}")
            

        if video:
            print(f"Fetching movies with video set to False")
            return self.download_movie(language, page, video=False, adult=adult)
        elif adult:
            print(f"Fetching movies with adult set to False")
            return self.download_movie(language, page, video=video, adult=False)

        return movie_downloads
    
    def set_genres_with_movie(self,movie):
        genres = movie['genre_ids']
        movie_id = movie['id']

        if not self.db_session.query(GenreMovie).filter(GenreMovie.id_movie == movie_id) is None:
            
            if len(genres) == 1:
                associaton = GenreMovie(
                    id_genre = genres[0],
                    id_movie = movie_id
                )
                self.db_session.add(associaton)
                self.db_session.commit()
            else:
                for genre in genres:
                    associaton = GenreMovie(
                        id_genre = genre,
                        id_movie = movie_id
                    )
                    self.db_session.add(associaton)
                    self.db_session.commit()

    # def movie_by_name(self,name,lang):
    #     existing_movie = self.db_session.query(Movie).filter(Movie.title == name).first()
    #     if existing_movie is None:

    def api_start(self,url):
        return requests.get(url, headers={
            "accept": "application/json",
            "Authorization": os.getenv('header_authorization')
        }).json()



