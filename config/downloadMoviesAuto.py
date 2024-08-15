from dotenv import load_dotenv
import os
import logging
import requests

def automated_download_movies():
    load_dotenv()
    url = os.getenv("URL_FOR_AUTOMATIC_DOWNLOAD_MOVIES")
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    logging.info(f"HTTP Status Code: {response.status_code}")
    logging.info(f"Response Text: {response.text}")
    if response.status_code == 200:
        try:
            response_json = response.json()
            logging.info("Respuesta automática del endpoint de descarga de peliculas: %s", response_json)
        except requests.exceptions.JSONDecodeError:
            logging.error(f"Error decoding JSON from response: {response.text}")
    else:
        logging.error("Respuesta automática del endpoint de descarga de peliculas: %s     , ERROR : %s", response.status_code, response.text)