import requests
import environ
import os
from pathlib import Path
import json
from requests.exceptions import HTTPError

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()


class cliente_api:
    
    def __init__(self, token, metodo, url, datos_envio=None, formato_respuesta="json"):
        self.token = token        
        self.metodo = metodo.upper()  # Convertir método a mayúsculas por seguridad
        self.url = url
        self.datos_envio = datos_envio
        self.formato_respuesta = formato_respuesta
        self.codigo_respuesta = 0
        self.datos_respuesta = {}
        self.headers = {}

    def crear_cabecera(self):
        """Crea los headers incluyendo el token"""
        self.headers["Authorization"] = f"Bearer {self.token}"
        if self.metodo in ["PUT", "PATCH", "POST"]:
            self.headers["Content-Type"] = "application/json"

    def transformar_datos_envio(self):
        """Convierte los datos a JSON si es necesario"""
        if self.datos_envio is not None and isinstance(self.datos_envio, dict):
            self.datos_envio = json.dumps(self.datos_envio)

    def realizar_peticion(self):
        """Realiza la petición HTTP según el método especificado"""
        try:
            url_completa = f"http://127.0.0.1:8000/{self.url}"
            
            metodos_http = {
                "GET": requests.get,
                "POST": requests.post,
                "PUT": requests.put,
                "PATCH": requests.patch,
                "DELETE": requests.delete,
            }

            if self.metodo in metodos_http:
                self.respuesta = metodos_http[self.metodo](url_completa, headers=self.headers, data=self.datos_envio)
            else:
                raise ValueError("Método HTTP no válido.")

            self.codigo_respuesta = self.respuesta.status_code
            self.respuesta.raise_for_status()

        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {repr(http_err)}')
        except Exception as err:
            print(f'Ocurrió un error inesperado: {repr(err)}')

    def tratar_respuesta(self):
        """Convierte la respuesta en JSON si corresponde"""
        if self.formato_respuesta == "json" and self.respuesta is not None:
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
            print(f'Ocurrió un error: {repr(err)}')

    def es_respuesta_correcta(self):
        return self.codigo_respuesta in [200, 201]  # También consideramos 201 como respuesta válida

    def es_error_validacion_datos(self):
        return self.codigo_respuesta == 400

    def incluir_errores_formulario(self, formulario):
        errores = self.datos_respuesta
        for error in errores:
            formulario.add_error(error, errores[error])