import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    # Path to your Firebase Admin SDK key
    path_to_key = '/etc/secrets/family-film-app-firebase-adminsdk-qr49b-762ab41ed8.json'
    
    cred = credentials.Certificate(path_to_key)
    firebase_app = firebase_admin.initialize_app(cred)
    return firebase_app
