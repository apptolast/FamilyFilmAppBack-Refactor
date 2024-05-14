from dotenv import load_dotenv
import os
import logging
import requests

def automated_download_movies():
    load_dotenv()
    url = os.getenv("URL_FOR_AUTOMATIC_DOWNLOAD_MOVIES")
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logging.info("Respuesta automática del endpoint de descarga de peliculas funcion que se ejecuta automatica : %s     , ERROR : %s", response.status_code, response.text)