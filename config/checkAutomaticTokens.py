import logging
import requests

from config.readJsonUsers import read_json_users_file
from dotenv import load_dotenv
import os

def check_token_validation():
    load_dotenv()
    url = os.getenv("URL_FOR_AUTOMATIC_RENEW_TOKEN")
    headers = {'Content-Type': 'application/json'}
    payload = {"email": read_json_users_file()}
    response = requests.post(url, headers=headers, json=payload)
    logging.info("Respuesta automática del endpoint: %s", response.json())