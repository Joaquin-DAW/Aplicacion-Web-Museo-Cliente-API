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
    
    def obtener_exposicion(exposicion_id):
        """
        Obtiene los datos de una exposición por su ID desde la API.
        """
        headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO")}
        url = f"http://127.0.0.1:8000/api/v1/exposiciones/{exposicion_id}"

        try:
            response = requests.get(url, headers=headers)
            print("📡 Respuesta de la API:", response.status_code, response.text)  # 🔍 Debug

            if response.status_code == 200:
                return response.json()  # ✅ Retorna los datos de la exposición
            elif response.status_code == 404:
                print("⚠️ Exposición no encontrada (404)")
            else:
                print("❌ Error en la API al obtener exposición:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("🚨 Error de conexión con la API:", e)

        return None  # ❌ Si hay error, devuelve None