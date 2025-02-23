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
    
    def obtener_visita_guiada(visita_id):
        """
        Obtiene los datos de una visita guiada por su ID desde la API.
        """
        headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO")}
        url = f"http://127.0.0.1:8000/api/v1/visitasguiadas/{visita_id}"

        try:
            response = requests.get(url, headers=headers)
            print("📡 Respuesta de la API:", response.status_code, response.text)  # 🔍 Debug

            if response.status_code == 200:
                return response.json()  # ✅ Retorna los datos de la visita guiada
            elif response.status_code == 404:
                print("⚠️ Visita guiada no encontrada (404)")
            else:
                print("❌ Error en la API al obtener visita guiada:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("🚨 Error de conexión con la API:", e)

        return None  # ❌ Si hay error, devuelve None
    
    def obtener_tiendas():
        """
        Obtiene la lista de tiendas disponibles desde la API.
        """
        headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO")}
        url = "http://127.0.0.1:8000/api/v1/tiendas"

        try:
            response = requests.get(url, headers=headers)
            print("📡 Respuesta de la API (Tiendas):", response.status_code, response.text)  # 🔍 Debug

            if response.status_code == 200:
                tiendas = response.json()
                return [(tienda["id"], tienda["nombre"]) for tienda in tiendas]
            elif response.status_code == 404:
                print("⚠️ No se encontraron tiendas disponibles (404)")
            else:
                print("❌ Error en la API al obtener tiendas:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("🚨 Error de conexión con la API:", e)

        return []  # Devuelve lista vacía en caso de error
    
    
def obtener_producto(producto_id):
    """
    Obtiene los datos de un producto por su ID desde la API.
    """
    headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO")}
    url = f"http://127.0.0.1:8000/api/v1/productos/{producto_id}"

    try:
        response = requests.get(url, headers=headers)
        print("📡 Respuesta de la API:", response.status_code, response.text)  # 🔍 Debug

        if response.status_code == 200:
            producto = response.json()
        
            # Obtener detalles de Inventario para cada tienda asociada
            for inventario in producto.get("inventario", []):
                tienda_id = inventario["tienda_id"]
                tienda_data = requests.get(f"http://127.0.0.1:8000/api/v1/tiendas/{tienda_id}", headers=headers)
                if tienda_data.status_code == 200:
                    inventario["tienda_nombre"] = tienda_data.json().get("nombre", "Desconocido")

            return producto  # Retorna el producto con detalles de Inventario
        
        elif response.status_code == 404:
            print("⚠️ Producto no encontrado (404)")
        else:
            print("❌ Error en la API al obtener producto:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("🚨 Error de conexión con la API:", e)

    return None  # ❌ Si hay error, devuelve None


def actualizar_producto(producto_id, datos):
    """
    Envía una solicitud PUT a la API para actualizar un producto.
    Maneja respuestas y errores.
    """
    url_correcta = f"http://127.0.0.1:8000/api/v1/productos/editar/{producto_id}/"
    print(f"🔗 Enviando petición PUT a: {url_correcta}")

    headers = {
        "Authorization": f"Bearer {env('TOKEN_ACCESO')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.put(url_correcta, headers=headers, json=datos)
        print(f"📡 Respuesta de la API ({response.status_code}): {response.text}")

        if response.status_code == 200:
            return {"success": True, "message": "Producto actualizado correctamente."}
        elif response.status_code == 400:
            return {"success": False, "message": "Error en la validación de datos.", "status": 400}
        elif response.status_code == 404:
            return {"success": False, "message": "Producto no encontrado.", "status": 404}
        else:
            return {"success": False, "message": f"Error inesperado: {response.text}", "status": response.status_code}
    
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión con la API: {e}")
        return {"success": False, "message": "Error de conexión con la API.", "status": 500}
