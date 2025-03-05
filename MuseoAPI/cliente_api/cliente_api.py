import requests
import environ
import os
from pathlib import Path
import json
from requests.exceptions import HTTPError, RequestException

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"), True)
env = environ.Env()

API_BASE_URL = "http://127.0.0.1:8000/api/v1/"  # Modifica según el entorno

class cliente_api:
    def __init__(self, token="", metodo="GET", url="", datos_envio=None, formato_respuesta="json"):
        self.token = token
        self.metodo = metodo.upper()  # Convertimos método a mayúsculas
        self.url = url
        self.datos_envio = datos_envio
        self.formato_respuesta = formato_respuesta
        self.codigo_respuesta = None  # Inicializamos para evitar errores
        self.datos_respuesta = {}
        self.headers = {}
        self.respuesta = None

    def crear_cabecera(self):
        """Crea los headers incluyendo el token de autenticación si se proporciona"""
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
        if self.metodo in ["POST", "PUT", "PATCH"]:
            self.headers["Content-Type"] = "application/json"

    def transformar_datos_envio(self):
        """Convierte los datos a JSON si es necesario"""
        if self.datos_envio is not None and isinstance(self.datos_envio, dict):
            self.datos_envio = json.dumps(self.datos_envio)

    def realizar_peticion(self):
        """Realiza la petición HTTP según el método especificado"""
        try:
            # Eliminar posible repetición de "api/v1/"
            if self.url.startswith("api/v1/"):
                self.url = self.url.replace("api/v1/", "", 1)
            
            url_completa = API_BASE_URL + self.url

            metodos_http = {
                "GET": requests.get,
                "POST": requests.post,
                "PUT": requests.put,
                "PATCH": requests.patch,
                "DELETE": requests.delete,
            }

            if self.metodo in metodos_http:
                self.respuesta = metodos_http[self.metodo](
                    url_completa, headers=self.headers, data=self.datos_envio
                )
            else:
                raise ValueError(f"Método HTTP no válido: {self.metodo}")

            self.codigo_respuesta = self.respuesta.status_code
            self.respuesta.raise_for_status()  # Lanza error si la respuesta no es 2xx

        except HTTPError as http_err:
            print(f"⚠️ Error HTTP: {repr(http_err)}")
            self.codigo_respuesta = self.respuesta.status_code if self.respuesta else 500
        except RequestException as err:
            print(f"🚨 Error en la petición: {repr(err)}")
            self.codigo_respuesta = 500

    def tratar_respuesta(self):
        """Convierte la respuesta en JSON si corresponde"""
        if self.respuesta and self.formato_respuesta == "json":
            try:
                self.datos_respuesta = self.respuesta.json()
            except json.JSONDecodeError:
                self.datos_respuesta = {}

    def realizar_peticion_api(self):
        """Ejecuta todo el proceso de la petición API"""
        try:
            self.crear_cabecera()
            self.transformar_datos_envio()
            self.realizar_peticion()
            self.tratar_respuesta()
        except Exception as err:
            self.codigo_respuesta = 500
            print(f"Error inesperado: {repr(err)}")

    def es_respuesta_correcta(self):
        return self.codigo_respuesta in [200, 201]

    def es_error_validacion_datos(self):
        return self.codigo_respuesta == 400

    def incluir_errores_formulario(self, formulario):
        """Añade errores a un formulario Django basado en la respuesta de la API"""
        if self.datos_respuesta:
            for error, mensaje in self.datos_respuesta.items():
                formulario.add_error(error, mensaje)
