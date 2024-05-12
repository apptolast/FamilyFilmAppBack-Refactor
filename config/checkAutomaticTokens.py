import requests

from config.readJsonUsers import read_json_users_file

def check_token_validation():
    url = "http://0.0.0.0:9900/users/automated/token"
    headers = {
            'Content-Type': 'application/json'
    }
    payload = {
        "email": read_json_users_file()
    }
    response = requests.post(url, headers=headers, json=payload)
    print("QUIERO QUE ME IMPRIMA LA RESPUESTA DE AQUI PRO EL DOCKER")
    print(f"Respuesta automática DEL ENDPOINT: {response.json()}")