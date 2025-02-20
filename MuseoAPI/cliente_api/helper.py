import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

class helper:
    
    def obtener_museo(museo_id):
        headers = {'Authorization': 'Bearer '+env("TOKEN_ACCESO")} 
        response = requests.get(f'http://127.0.0.1:8000/api/v1/museos/{museo_id}', headers=headers)
        
        if response.status_code == 200:
            return response.json()
        return None