import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    path_to_key = '/etc/secrets/JSON_FILE'
    cred = credentials.Certificate(path_to_key)
    firebase_app = firebase_admin.initialize_app(cred)
    return firebase_app
