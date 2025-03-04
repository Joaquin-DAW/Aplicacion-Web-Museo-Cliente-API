import requests
from django.shortcuts import render, redirect
from .forms import *
import xml.etree.ElementTree as ET #Importamos la librería para trabajar con XML
from django.contrib import messages
from datetime import datetime
from .cliente_api import cliente_api
from .helper import helper
from .helper import *
from requests.exceptions import HTTPError
import json
import logging

# Configurar logging para que los errores aparezcan en la consola
logger = logging.getLogger(__name__)

import requests
import environ
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

# Para mejorar el uso de la url y no tener que cambiarla en cada línea que la usaramos cuando sufra un cambio podemos 
# almacenar la url de la API en una variable global llamada "API_BASE_URL" que guardamos en el .env (también podemos guardarla en settings.py)

# Si necesitaramos cambiar la url de la API, o su versión, o cualquier parametro de configuración que estuviera registrado en la url solo 
# necesitamos modificar el archivo .env en lugar de tener que cambiar los valores de la url vista por vista de este archivo.

API_BASE_URL = env("API_BASE_URL")


# Si queremos poder manejar diferentes formatos de respuesta lo que tendremos que hacer primero es identificar el formato de la respuesta que tenemos que devolver
# para luego poder devolverla en el formato que necesitemos. 
# Para ello podemos crear una función que nos devuelva el tipo de respuesta que tenemos que devolver, en nuestro caso sera "tipo_respuesta" que se 
# envarga de recibir la respuesta de la API.
# Gracias a esto evitaremos tener que modificar el codigo si en un futuro cambiamos el formato de respuesta de la API.


# No siempre es necesario controlar todos los errores, pero si es cierto que en las partes más complejas de nuestra aplicación es recomendable, como por ejemplo en la busqueda avanzada.
# en los formularios avanzados.

# Vamos a controlar los errores más importantes que podemos encontrarnos en una aplicacion web, el 400, 401, 404 y los errores del servidor (500 o superiores).
# Para ello vamos a modificar la función "tipo_respuesta" para que devuelva un diccionario con un mensaje de error en caso de que se produzca un error en la respuesta.
# Nos centraremos en controlarlo en la parte más compleja de nuestra app, es decir en la de la busqueda avanzada, ya que es la que más interacciones con la API tiene.

def tipo_respuesta(response):

    if response.status_code == 200:
        if response.headers.get("Content-Type") == "application/json": # Si la respuesta es JSON devuelve un diccionario
            return response.json()
        elif response.headers.get("Content-Type") == "application/xml": # Si la respuesta es XML la convierte a diccionario
            root = ET.fromstring(response.text)
            return {child.tag: child.text for child in root}  # Conversión básica de XML a diccionario
        else:
            return {"error": "Formato de respuesta no soportado"}
    
    elif response.status_code == 400:
        try:
            return response.json()  # Intenta obtener detalles del error si la API los proporciona
        except ValueError:
            return {"error": "Solicitud incorrecta", "detalles": response.text}
    
    elif response.status_code == 401:
        return {"error": "No autorizado. Inicia sesión para continuar."}
    
    elif response.status_code == 404:
        return {"error": "Recurso no encontrado. Verifica la URL o los parámetros."}
    
    elif response.status_code >= 500:
        return {"error": "Error en el servidor. Inténtalo más tarde."}
    
    return {"error": f"Error inesperado: {response.status_code}"}
    
# Ahora cambiamos el response.json() por tipo_respuesta(response) en las llamadas a la API para que se encargue de devolver el formato correcto.


def index(request):
    return render(request, 'index.html')

def crear_cabecera():
    return {
        'Authorization': 'Bearer '+env("TOKEN_ACCESO"),
        "Content-Type": "application/json"
    }

def listar_museos(request):
    #Obtenemos todos los museos
    headers = crear_cabecera() 
    response = requests.get(f'{API_BASE_URL}museos', headers=headers)
    #Transformamos la respuesta en json
    if response.status_code == 404:
        return tratar_errores(request, 404) 
        
    museos = tipo_respuesta(response)

    if "error" in museos:
        return tratar_errores(request, 500)
    
    return render(request, 'museo/lista.html',{"museos":museos})

def listar_obras(request):
    headers = crear_cabecera() 
    response = requests.get(f'{API_BASE_URL}obras', headers=headers)
    if response.status_code == 404:
        return tratar_errores(request, 404)

    obras = tipo_respuesta(response)

    if "error" in obras:
         return tratar_errores(request, 500)
    
    return render(request, 'obra/lista.html', {'obras': obras})

def listar_exposiciones(request):
    headers = crear_cabecera() 
    response = requests.get(f'{API_BASE_URL}exposiciones', headers=headers)
    if response.status_code == 404:
        return tratar_errores(request, 404)

    exposiciones = tipo_respuesta(response)

    if "error" in exposiciones:
        return tratar_errores(request, 500)
    
    if "error" in exposiciones:
        return render(request, 'museo/lista.html', {"error": exposiciones["error"]})
    
    return render(request, 'exposicion/lista.html', {'exposiciones': exposiciones})

def listar_artistas(request):
    headers = crear_cabecera() 
    response = requests.get(f'{API_BASE_URL}artistas', headers=headers)
    if response.status_code == 404:
        return tratar_errores(request, 404)
       

    artistas = tipo_respuesta(response)

    if "error" in artistas:
        return tratar_errores(request, 500)
    
    return render(request, 'estructura/artista/lista.html', {'artistas': artistas})

def listar_entradas(request):
    headers = crear_cabecera() 
    response = requests.get(f'{API_BASE_URL}entradas', headers=headers)
    if response.status_code == 404:
        return tratar_errores(request, 404)

    entradas = tipo_respuesta(response)

    if "error" in entradas:
        return tratar_errores(request, 500)
    
    return render(request, 'entrada/lista.html', {'entradas': entradas})

def listar_visitas_guiadas(request):
    # Obtener todas las visitas guiadas desde la API
    headers = crear_cabecera()
    response = requests.get(f'{API_BASE_URL}visitasguiadas', headers=headers)

    if response.status_code == 404:
        return tratar_errores(request, 404)

    visitas = tipo_respuesta(response)

    if "error" in visitas:
        return tratar_errores(request, 500)

    return render(request, 'visita_guiada/lista.html', {"visitas": visitas})


def museo_buscar_simple(request):
    if request.GET:
        formulario = BusquedaMuseoForm(request.GET)
        if formulario.is_valid():
            texto = formulario.cleaned_data.get("textoBusqueda")

            headers = crear_cabecera()
            response = requests.get(
                f'{API_BASE_URL}museos/busqueda_simple',
                headers=headers,
                params={'textoBusqueda': texto}
            )

            if response.status_code == 404:
                    return tratar_errores(request, 404)
            elif response.status_code == 500:
                    return tratar_errores(request, 500)

            response.raise_for_status()
                
            museos = tipo_respuesta(response)
            
            if response.status_code == 200:
                # La respuesta es correcta, procesamos los museos
                museos = response.json()
                return render(request, 'museo/lista_busqueda.html', {"museos": museos})

            elif response.status_code == 400:
                # Controlamos un error 400, si la API devuelve un error
                errores = response.json()
                return render(request, 'museo/busqueda_simple.html', {
                    "formulario": formulario,
                    "errores": errores
                })
            
            elif response.status_code == 401:
                # Manejo de error 401 (no autorizado)
                return render(request, 'museo/busqueda_simple.html', {
                    "formulario": formulario,
                    "error": "No autorizado. Por favor, inicie sesión."
                })
            
            elif response.status_code == 404:
                # Manejo de error 404 (no encontrado)
                return render(request, 'museo/busqueda_simple.html', {
                    "formulario": formulario,
                    "error": "No se han encontrado resultados para su búsqueda."
                })
            
            elif response.status_code == 500:
                # Manejo de error 500 (error interno del servidor)
                return render(request, 'museo/busqueda_simple.html', {
                    "formulario": formulario,
                    "error": "Hubo un error en el servidor. Inténtelo de nuevo más tarde."
                })
            
            else:
                # Si ocurre otro código de estado, podemos agregar un manejo general
                return render(request, 'museo/busqueda_simple.html', {
                    "formulario": formulario,
                    "error": "Hubo un error inesperado. Inténtelo de nuevo."
                })
        
        else:
            # Si el formulario no es válido, mostramos el formulario con los errores
            return render(request, 'museo/busqueda_simple.html', {"formulario": formulario})
    
    formulario = BusquedaMuseoForm()
    return render(request, 'museo/busqueda_simple.html', {"formulario": formulario})


def museo_buscar_avanzada(request):
    if request.GET:
        formulario = BusquedaAvanzadaMuseoForm(request.GET)

        if formulario.is_valid():
            headers = crear_cabecera()
            response = requests.get(
                f'{API_BASE_URL}museos/busqueda_avanzada/',
                headers=headers,
                params=formulario.cleaned_data
            )
            
            if response.status_code == 404:
                    return tratar_errores(request, 404)
            elif response.status_code == 500:
                    return tratar_errores(request, 500)

            response.raise_for_status()

            # Manejar errores específicos
            if response.status_code == 400:
                errores = response.json()  # Captura los errores del servidor
                return render(request, 'museo/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "errores": errores,
                })
            elif response.status_code == 401:
                return render(request, 'museo/error.html', {
                    "mensaje": "No tienes permisos para acceder a esta información. Por favor, inicia sesión."
                })
            elif response.status_code == 404:
                return render(request, 'museo/error.html', {
                    "mensaje": "No se encontraron museos que coincidan con tu búsqueda."
                })
            elif response.status_code == 500:
                return render(request, 'museo/error.html', {
                    "mensaje": "Lo sentimos, algo salió mal en el servidor. Por favor, intenta más tarde."
                })

            # Si la respuesta es correcta (200), procesar la respuesta
            museos = tipo_respuesta(response)
            return render(request, 'museo/lista_busqueda.html', {"museos": museos, "formulario": formulario})

    formulario = BusquedaAvanzadaMuseoForm()
    return render(request, 'museo/busqueda_avanzada.html', {"formulario": formulario})

# POST
def museo_create(request):
    if request.method == "POST":
        formulario = MuseoForm(request.POST)
        if formulario.is_valid():
            try:
                datos = formulario.cleaned_data.copy()
                datos["fecha_fundacion"] = datos["fecha_fundacion"].strftime("%Y-%m-%d")

                token = request.session.get("token", None)  #Obtener el token de sesión
                if not token:
                    messages.error(request, "No se encontró el token de autenticación.")
                    return redirect("login")

                cliente = cliente_api(token, "POST", "api/v1/museos/crear", datos)
                cliente.realizar_peticion_api()

                if cliente.es_respuesta_correcta():
                    messages.success(request, "El museo se ha creado correctamente.")
                    return redirect("listar_museos")
                else:
                    errores = cliente.datos_respuesta
                    for error in errores:
                        formulario.add_error(error, errores[error])
            except Exception as err:
                messages.error(request, f"Ocurrió un error: {err}")
    else:
        formulario = MuseoForm()
    
    return render(request, "museo/create.html", {"formulario": formulario})


# PUT - Editar un museo
def museo_editar(request, museo_id):
    datosFormulario = None

    if request.method == "POST":
        datosFormulario = request.POST

    # Obtener museo desde la API
    museo = helper.obtener_museo(museo_id)
    if museo is None:
        return tratar_errores(request, 404)

    # Crear formulario con datos iniciales
    formulario = MuseoForm(
        datosFormulario,
        initial={
            'nombre': museo['nombre'],
            'ubicacion': museo['ubicacion'],
            'fecha_fundacion': datetime.strptime(museo['fecha_fundacion'], '%Y-%m-%d').date(),
            'descripcion': museo['descripcion']
        }
    )

    if request.method == "POST" and formulario.is_valid():
        datos = formulario.cleaned_data.copy()
        datos["fecha_fundacion"] = datos["fecha_fundacion"].strftime('%Y-%m-%d')

        # Obtener token del usuario autenticado
        token = request.session.get("token", None)
        if not token:
            messages.error(request, "No se encontró el token de autenticación.")
            return redirect("login")

        # Usar `cliente_api` para la petición
        try:
            cliente = cliente_api(token, "PUT", f"api/v1/museos/editar/{museo_id}", datos)
            cliente.realizar_peticion_api()

            if cliente.es_respuesta_correcta():
                messages.success(request, "El museo ha sido actualizado correctamente.")
                return redirect("listar_museos")
            elif cliente.es_error_validacion_datos():
                cliente.incluir_errores_formulario(formulario)
            else:
                messages.error(request, "Error al actualizar el museo.")
                print("Código HTTP:", cliente.codigo_respuesta)
                print("Detalles del error:", cliente.datos_respuesta)

        except requests.exceptions.RequestException as err:
            messages.error(request, f"Error de conexión al actualizar el museo: {err}")
            return tratar_errores(request, 500)

    return render(request, "museo/actualizar.html", {"formulario": formulario, "museo": museo})


def museo_editar_nombre(request, museo_id):
    datosFormulario = None
    museo = helper.obtener_museo(museo_id)  

    formulario = MuseoEditarNombreForm(
        datosFormulario,
        initial={'nombre': museo['nombre']}
    )

    if request.method == "POST":
        try:
            formulario = MuseoEditarNombreForm(request.POST)
            datos = request.POST.copy()

            token = request.session.get("token", None)
            if not token:
                messages.error(request, "No se encontró el token de autenticación.")
                return redirect("login")

            # Usar `cliente_api` para la petición PATCH
            cliente = cliente_api(token, "PATCH", f"api/v1/museos/editar/nombre/{museo_id}", datos)
            cliente.realizar_peticion_api()

            if cliente.es_respuesta_correcta():
                messages.success(request, "Nombre del museo actualizado correctamente.")
                return redirect("listar_museos")
            else:
                messages.error(request, "Error al actualizar el nombre del museo.")
                print("Código HTTP:", cliente.codigo_respuesta)
                print("Detalles del error:", cliente.datos_respuesta)

        except requests.exceptions.RequestException as err:
            messages.error(request, f"Error de conexión: {err}")
            return tratar_errores(request, 500)

    return render(request, 'museo/actualizar_nombre.html', {"formulario": formulario, "museo": museo})

def museo_eliminar(request, museo_id):
    try:
        token = request.session.get("token", None)
        if not token:
            messages.error(request, "No se encontró el token de autenticación.")
            return redirect("login")

        # Usar `cliente_api` para la petición DELETE
        cliente = cliente_api(token, "DELETE", f"api/v1/museos/eliminar/{museo_id}")
        cliente.realizar_peticion_api()

        if cliente.es_respuesta_correcta():
            messages.success(request, "Museo eliminado correctamente.")
        else:
            messages.error(request, "No se pudo eliminar el museo.")
            print("Código HTTP:", cliente.codigo_respuesta)
            print("Detalles del error:", cliente.datos_respuesta)

    except Exception as err:
        messages.error(request, f"Ocurrió un error: {err}")

    return redirect("listar_museos")


def obra_buscar_avanzada(request):
    if request.GET:
        formulario = BusquedaAvanzadaObraForm(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"

            headers = crear_cabecera()
            
            # Realiza la llamada GET a la API para la búsqueda avanzada de obras
            response = requests.get(
                f'{API_BASE_URL}obras/busqueda_avanzada/',
                headers=headers,
                params=formulario.cleaned_data
            )
            
            if response.status_code == 404:
                return tratar_errores(request, 404)
            elif response.status_code == 500:
                return tratar_errores(request, 500)
            
            response.raise_for_status()
            
            obras = tipo_respuesta(response)
            
            if response.status_code == 200:
                obras = response.json()
                return render(request, 'obra/lista_busqueda.html', {
                    "obras": obras,
                    "mensaje_busqueda": mensaje_busqueda,
                    "formulario": formulario
                })
            elif response.status_code == 400:
                # Control de error 400
                errores = response.json() 
                return render(request, 'obra/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "errores": errores
                })
            elif response.status_code == 401:
                # Control de error 401
                return render(request, 'obra/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": "No autorizado. Por favor, inicie sesión."
                })
            elif response.status_code == 404:
                # Control de error 404
                return render(request, 'obra/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": "No se han encontrado obras con los criterios de búsqueda."
                })
            elif response.status_code == 500:
                # Control de error 500
                return render(request, 'obra/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": "Hubo un error en el servidor. Inténtelo de nuevo más tarde."
                })
            else:
                # Otro tipo de error
                return render(request, 'obra/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": f"Error inesperado: {response.status_code}"
                })
        else:
            return render(request, 'obra/busqueda_avanzada.html', {
                "formulario": formulario,
                "errores": formulario.errors
            })
    else:
        formulario = BusquedaAvanzadaObraForm()
        return render(request, 'obra/busqueda_avanzada.html', {"formulario": formulario})
    
# POST
def exposicion_create(request):
    """
    Crea una nueva exposición enviando los datos a la API con control de autenticación.
    """
    if request.method == "POST":
        formulario = ExposicionForm(request.POST)
        if formulario.is_valid():
            
            # Copiar datos del formulario
            datos = formulario.cleaned_data.copy()

            # Convertir fechas a string en formato "YYYY-MM-DD"
            datos["fecha_inicio"] = datos["fecha_inicio"].strftime("%Y-%m-%d")
            if datos["fecha_fin"]:
                datos["fecha_fin"] = datos["fecha_fin"].strftime("%Y-%m-%d")

            # Asegurar que el ID del museo sea un número entero
            datos["museo"] = int(formulario.cleaned_data["museo"])

            # Obtener el token de sesión del usuario autenticado
            token = request.session.get("token", None)
            if not token:
                messages.error(request, "No se encontró el token de autenticación.")
                return redirect("login")

            print("📡 Datos que se enviarán a la API:", datos)  # 🔍 Debug

            # Usar `cliente_api` para la petición
            cliente = cliente_api(token, "POST", "api/v1/exposiciones/crear", datos)
            cliente.realizar_peticion_api()

            if cliente.es_respuesta_correcta():
                messages.success(request, "La exposición se ha creado correctamente.")
                return redirect("listar_exposiciones")
            else:
                messages.error(request, "Error al crear la exposición.")
                print("Código HTTP:", cliente.codigo_respuesta)
                print("Detalles del error:", cliente.datos_respuesta)

    else:
        formulario = ExposicionForm()  

    return render(request, "exposicion/create.html", {"formulario": formulario})


# PUT - Editar una exposición
def exposiciones_editar(request, exposicion_id):
    datosFormulario = None

    if request.method == "POST":
        datosFormulario = request.POST

    # Obtener la exposición desde la API
    exposicion = helper.obtener_exposicion(exposicion_id)
    
    if exposicion is None:
            return tratar_errores(request, 404)

    if exposicion is None:  # 🚨 Evita el error si `exposicion` no existe
        messages.error(request, "No se pudo obtener la exposición. Verifica que exista y que la API esté funcionando correctamente.")
        return redirect("listar_exposiciones")  # 🔹 Redirige para evitar el error

    # Crear el formulario con los datos iniciales de la exposición
    formulario = ExposicionForm(
        datosFormulario,
        initial={
            'titulo': exposicion.get('titulo', ''),  # ✅ Usa `.get()` para evitar errores si falta el campo
            'fecha_inicio': datetime.strptime(exposicion['fecha_inicio'], '%Y-%m-%d').date(),
            'fecha_fin': datetime.strptime(exposicion['fecha_fin'], '%Y-%m-%d').date() if exposicion.get('fecha_fin') else None,
            'descripcion': exposicion.get('descripcion', ''),
            'capacidad': exposicion.get('capacidad', 0),
            'museo': exposicion.get('museo', '')  # 🔹 Asegura que se pase correctamente
        }
    )

    # Si el formulario es enviado con método POST y es válido
    if request.method == "POST" and formulario.is_valid():
        datos = formulario.cleaned_data.copy()
        datos["fecha_inicio"] = datos["fecha_inicio"].strftime('%Y-%m-%d')
        if datos["fecha_fin"]:
            datos["fecha_fin"] = datos["fecha_fin"].strftime('%Y-%m-%d')

        datos["museo"] = int(datos["museo"])  # ✅ Convertimos el ID del museo a entero

        url_correcta = f"api/v1/exposiciones/editar/{exposicion_id}"
        print("🔗 Endpoint generado:", url_correcta)  # 🔹 Debug

        cliente = cliente_api(env("TOKEN_ACCESO"), "PUT", url_correcta, datos)
        cliente.realizar_peticion_api()

        if cliente.es_respuesta_correcta():
            messages.success(request, "La exposición ha sido actualizada correctamente.")
            return redirect("listar_exposiciones")
        elif cliente.es_error_validacion_datos():
            cliente.incluir_errores_formulario(formulario)
        else:
            print("❌ ERROR: Ocurrió un problema en la actualización de la exposición.")  
            print("📡 Enviando petición PUT a:", f'{API_BASE_URL}exposiciones/editar/{exposicion_id}')
            return tratar_errores(request, cliente.codigoRespuesta)

    return render(request, "exposicion/actualizar.html", {"formulario": formulario, "exposicion": exposicion})

#PATCH
def exposicion_editar_capacidad(request, exposicion_id):
    datosFormulario = None
    exposicion = helper.obtener_exposicion(exposicion_id)  # Obtenemos la exposición

    formulario = ExposicionEditarCapacidadForm(
        datosFormulario,
        initial={'capacidad': exposicion['capacidad']}
    )
    
    if request.method == "POST":
        try:
            formulario = ExposicionEditarCapacidadForm(request.POST)
            headers = crear_cabecera()
            datos = request.POST.copy()

            response = requests.patch(
                f"{API_BASE_URL}exposiciones/editar/capacidad/{exposicion_id}/",  # 📌 Endpoint correcto
                headers=headers,
                data=json.dumps(datos)
            )
            
            if response.status_code == 404:
                return tratar_errores(request, 404)
            elif response.status_code == 500:
                return tratar_errores(request, 500)
                    
            response.raise_for_status()

            if response.status_code == 200:
                messages.success(request, "Capacidad de la exposición actualizada correctamente.")
                return redirect("listar_exposiciones")
            else:
                print(response.status_code)
                response.raise_for_status()

        except requests.exceptions.HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'exposicion/actualizar_capacidad.html', {"formulario": formulario, "exposicion": exposicion})
            else:
                print("❌ ERROR: Ocurrió un problema en la actualización de la exposición.")  
                print("📡 Enviando petición PATCH a:", f'{API_BASE_URL}exposiciones/editar/capacidad/{exposicion_id}')

            messages.error(request, "Error al actualizar la exposición. Revisa la consola para más detalles.") 
            return redirect("listar_exposiciones")

    return render(request, 'exposicion/actualizar_capacidad.html', {"formulario": formulario, "exposicion": exposicion})
    
def exposicion_buscar_avanzada(request):
    if request.GET:
        formulario = BusquedaAvanzadaExposicionForm(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            headers = crear_cabecera()  # Función que genera los headers (si necesitas autenticación o similar)

            # Realiza la llamada GET a la API para la búsqueda avanzada de exposiciones
            response = requests.get(
                f'{API_BASE_URL}exposiciones/busqueda_avanzada/',
                headers=headers,
                params=formulario.cleaned_data
            )
            
            if response.status_code == 404:
                return tratar_errores(request, 404)
            elif response.status_code == 500:
                return tratar_errores(request, 500)
            
            response.raise_for_status()

            exposiciones = tipo_respuesta(response)

            if response.status_code == 200:
                exposiciones = response.json()
                return render(request, 'exposicion/lista_busqueda.html', {
                    "exposiciones": exposiciones,
                    "mensaje_busqueda": mensaje_busqueda,
                    "formulario": formulario
                })
            elif response.status_code == 400:
                errores = response.json()  # Errores devueltos por el servidor
                return render(request, 'exposicion/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "errores": errores
                })
            elif response.status_code == 401:
                return render(request, 'exposicion/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": "No autorizado. Por favor, inicie sesión."
                })
            elif response.status_code == 404:
                return render(request, 'exposicion/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": "No se han encontrado exposiciones con los criterios de búsqueda."
                })
            elif response.status_code == 500:
                return render(request, 'exposicion/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": "Hubo un error en el servidor. Inténtelo de nuevo más tarde."
                })
            else:
                return render(request, 'exposicion/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": f"Error inesperado: {response.status_code}"
                })
        else:
            return render(request, 'exposicion/busqueda_avanzada.html', {
                "formulario": formulario,
                "errores": formulario.errors
            })
    else:
        formulario = BusquedaAvanzadaExposicionForm()
        return render(request, 'exposicion/busqueda_avanzada.html', {"formulario": formulario})
    
#Delete Exposicion
def exposicion_eliminar(request, exposicion_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            f'http://127.0.0.1:8000/api/v1/exposiciones/eliminar/{exposicion_id}',
            headers=headers,
        )
        
        if response.status_code == 404:
                return tratar_errores(request, 404)
        elif response.status_code == 500:
                return tratar_errores(request, 500)
            
        response.raise_for_status()
        
        if response.status_code == requests.codes.ok:
            messages.success(request, "Exposición eliminada correctamente.")
        else:
            messages.error(request, "No se pudo eliminar la exposición.")
    except Exception as err:
        messages.error(request, f"Ocurrió un error: {err}")

    return redirect("listar_exposiciones")  # Redirigir siempre a la lista de exposiciones
    
def entrada_buscar_avanzada(request):
    if request.GET:
        formulario = BusquedaAvanzadaEntradaForm(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            headers = crear_cabecera()

            # Realiza la llamada GET a la API para la búsqueda avanzada de entradas
            response = requests.get(
                f'{API_BASE_URL}entradas/busqueda_avanzada/',
                headers=headers,
                params=formulario.cleaned_data
            )

            if response.status_code == 404:
                return tratar_errores(request, 404)
            elif response.status_code == 500:
                return tratar_errores(request, 500)
            
            response.raise_for_status()

            entradas = tipo_respuesta(response)

            if response.status_code == 200:
                entradas = response.json()
                return render(request, 'entrada/lista_busqueda.html', {
                    "entradas": entradas,
                    "mensaje_busqueda": mensaje_busqueda,
                    "formulario": formulario
                })
            elif response.status_code == 400:
                errores = response.json()
                return render(request, 'entrada/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "errores": errores
                })
            elif response.status_code == 401:
                return render(request, 'entrada/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": "No autorizado. Por favor, inicie sesión."
                })
            elif response.status_code == 404:
                return render(request, 'entrada/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": "No se han encontrado entradas con los criterios de búsqueda."
                })
            elif response.status_code == 500:
                return render(request, 'entrada/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": "Hubo un error en el servidor. Inténtelo de nuevo más tarde."
                })
            else:
                return render(request, 'entrada/busqueda_avanzada.html', {
                    "formulario": formulario,
                    "error": f"Error inesperado: {response.status_code}"
                })
        else:
            return render(request, 'entrada/busqueda_avanzada.html', {
                "formulario": formulario,
                "errores": formulario.errors
            })
    else:
        formulario = BusquedaAvanzadaEntradaForm()
        return render(request, 'entrada/busqueda_avanzada.html', {"formulario": formulario})
    
# POST visita guiada    
def visita_guiada_create(request):
    print("✅ Se ha accedido a la vista de creación de visitas guiadas")  # 🔍 Verificar si se entra a la vista
    
    if request.method == "POST":
        print("✅ Se recibió una solicitud POST")  # 🔍 Comprobar que se detecta la petición POST
        formulario = VisitaGuiadaForm(request.POST)

        if formulario.is_valid():
            print("✅ El formulario es válido")  # 🔍 Confirmar que el formulario pasa validaciones
            
            datos = formulario.cleaned_data.copy()

            print("📡 Datos que se enviarán a la API:", datos)

            datos["guias"] = list(map(int, request.POST.getlist("guias")))
            datos["visitantes"] = list(map(int, request.POST.getlist("visitantes")))
            datos["duracion"] = f"0 {datos['duracion']}"  # Para asegurar compatibilidad con la API

            headers = crear_cabecera()

            response = requests.post(
                "http://127.0.0.1:8000/api/v1/visitasguiadas/crear",
                headers=headers,
                json=datos
            )
            
            if response.status_code == 404:
                return tratar_errores(request, 404)
            elif response.status_code == 500:
                return tratar_errores(request, 500)
            
            response.raise_for_status()

            print("📡 Respuesta del servidor:", response.status_code, response.text)

            if response.status_code == 201:
                messages.success(request, "La visita guiada se ha creado correctamente.")
                return redirect("listar_visitas_guiadas")

        else:
            print("❌ El formulario NO es válido")  # 🔍 Si no es válido, muestra los errores
            print(formulario.errors)

    else:
        formulario = VisitaGuiadaForm()
    
    return render(request, "visita_guiada/create.html", {"formulario": formulario})


#PUT de VisitaGuiada
def visita_guiada_editar(request, visita_id):
    print("✅ Accediendo a la vista de edición de visitas guiadas")  # 🔍 Verificar acceso

    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST

    # Obtener los datos de la visita guiada desde la API
    visita = helper.obtener_visita_guiada(visita_id)
    
    if visita is None:
            return tratar_errores(request, 404)

    if visita is None:  # 🚨 Evitar errores si la visita guiada no existe
        messages.error(request, "No se pudo obtener la visita guiada. Verifica que exista y que la API esté funcionando correctamente.")
        return redirect("listar_visitas_guiadas")  

    # Crear el formulario con los datos iniciales de la visita guiada
    formulario = VisitaGuiadaForm(
        datosFormulario,
        initial={
            'nombre_visita_guia': visita.get('nombre_visita_guia', ''),
            'duracion': str(visita.get('duracion', '')),
            'capacidad_maxima': visita.get('capacidad_maxima', 0),
            'idioma': visita.get('idioma', 'espanol'),
            'guias': visita.get('guias', []),  
            'visitantes': visita.get('visitantes', []),
        }
    )

    if request.method == "POST" and formulario.is_valid():
        datos = formulario.cleaned_data.copy()

        # Convertir la duración al formato adecuado
        datos["duracion"] = f"0 {datos['duracion']}"

        # Convertir IDs de ManyToMany a listas de enteros
        datos["guias"] = list(map(int, request.POST.getlist("guias")))
        datos["visitantes"] = list(map(int, request.POST.getlist("visitantes")))

        url_correcta = f"api/v1/visitasguiadas/editar/{visita_id}/"
        print("🔗 Endpoint generado:", url_correcta)

        cliente = cliente_api(env("TOKEN_ACCESO"), "PUT", url_correcta, datos)
        cliente.realizar_peticion_api()

        if cliente.es_respuesta_correcta():
            messages.success(request, "La visita guiada ha sido actualizada correctamente.")
            return redirect("listar_visitas_guiadas")
        elif cliente.es_error_validacion_datos():
            cliente.incluir_errores_formulario(formulario)
        else:
            print("❌ ERROR: Ocurrió un problema en la actualización de la visita guiada.")
            print("📡 Enviando petición PUT a:", f'{API_BASE_URL}visitasguiadas/editar/{visita_id}')
            return tratar_errores(request, cliente.codigoRespuesta)

    return render(request, "visita_guiada/actualizar.html", {"formulario": formulario, "visita": visita})


# PATCH - Editar solo la capacidad máxima de una visita guiada
def visita_guiada_editar_capacidad(request, visita_id):
    datosFormulario = None
    visita = helper.obtener_visita_guiada(visita_id)  # Obtiene la visita desde la API

    if not visita:
        messages.error(request, "No se pudo obtener la visita guiada.")
        return redirect("listar_visitas_guiadas")

    # Asegurar que la clave correcta está en el diccionario
    formulario = VisitaGuiadaEditarCapacidadForm(
        datosFormulario,
        initial={'capacidad_maxima': visita.get('capacidad_maxima', 1)}  # ✅ Usa el nombre correcto
    )

    if request.method == "POST":
        formulario = VisitaGuiadaEditarCapacidadForm(request.POST)

        if formulario.is_valid():
            try:
                headers = crear_cabecera()
                datos = request.POST.copy()

                response = requests.patch(
                    f"{API_BASE_URL}visitasguiadas/editar/capacidad/{visita_id}/",
                    headers=headers,
                    data=json.dumps(datos)
                )
                
                if response.status_code == 404:
                    return tratar_errores(request, 404)
                elif response.status_code == 500:
                    return tratar_errores(request, 500)
                
                response.raise_for_status()

                if response.status_code == 200:
                    messages.success(request, "Capacidad de la visita guiada actualizada correctamente.")
                    return redirect("listar_visitas_guiadas")
                else:
                    response.raise_for_status()

            except requests.exceptions.HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error, errores[error])
                    return render(request, 'visita_guiada/actualizar_capacidad.html', {"formulario": formulario, "visita": visita})
                else:
                    print("❌ ERROR: Ocurrió un problema en la actualización de la visita guiada.")
                    print("📡 Enviando petición PATCH a:", f'{API_BASE_URL}visitasguiadas/editar/capacidad/{visita_id}')

                messages.error(request, "Error al actualizar la visita guiada. Revisa la consola para más detalles.")
                return redirect("listar_visitas_guiadas")

    return render(request, 'visita_guiada/actualizar_capacidad.html', {"formulario": formulario, "visita": visita})

# DELETE Visita Guiada
def visita_guiada_eliminar(request, visita_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            f'http://127.0.0.1:8000/api/v1/visitasguiadas/eliminar/{visita_id}',
            headers=headers,
        )
        
        if response.status_code == 404:
                return tratar_errores(request, 404)
        elif response.status_code == 500:
                return tratar_errores(request, 500)
            
        response.raise_for_status()
        
        if response.status_code == requests.codes.ok:
            messages.success(request, "Visita guiada eliminada correctamente.")
        else:
            messages.error(request, "No se pudo eliminar la visita guiada.")
    except Exception as err:
        messages.error(request, f"Ocurrió un error: {err}")

    return redirect("listar_visitas_guiadas")  # Redirigir siempre a la lista de visitas guiadas


def listar_productos(request):
    headers = crear_cabecera()
    response = requests.get(f'{API_BASE_URL}productos', headers=headers)
    productos = tipo_respuesta(response)
    
    if response.status_code == 404:
            return tratar_errores(request, 404)
    elif response.status_code == 500:
            return tratar_errores(request, 500)
            
    response.raise_for_status()

    if "error" in productos:
        return render(request, 'producto/lista.html', {"error": productos["error"]})
    
    return render(request, 'producto/lista.html', {"productos": productos})


# POST Producto
def producto_create(request):
    print("✅ Se ha accedido a la vista de creación de productos")  

    if request.method == "POST":
        print("✅ Se recibió una solicitud POST")  
        formulario = ProductoForm(request.POST)

        if formulario.is_valid():
            print("✅ El formulario es válido")  

            datos = formulario.cleaned_data.copy()
            
            if datos.get("fecha_ultima_venta"):
                datos["fecha_ultima_venta"] = datos["fecha_ultima_venta"].isoformat()

            # Convertir Decimal a float para JSON
            datos["precio"] = float(datos["precio"])  

            print(" Datos que se enviarán a la API:", datos)

            headers = crear_cabecera()

            response = requests.post(
                "http://127.0.0.1:8000/api/v1/productos/crear",
                headers=headers,
                json=datos
            )
            
            if response.status_code == 404:
                return tratar_errores(request, 404)
            elif response.status_code == 500:
                return tratar_errores(request, 500)
            
            response.raise_for_status()

            print(" Respuesta del servidor:", response.status_code, response.text)

            if response.status_code == 201:
                messages.success(request, "El producto se ha creado correctamente.")
                return redirect("listar_productos")

        else:
            print(" El formulario NO es válido")  
            print(formulario.errors)

    else:
        formulario = ProductoForm()

    return render(request, "producto/create.html", {"formulario": formulario})

# PUT Producto
def producto_editar(request, producto_id):
    print("Accediendo a la vista de edición de productos")  # Debug
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST

    # Obtener los datos del producto desde la API usando helper
    producto = obtener_producto(producto_id)

    if producto is None:
        return tratar_errores(request, 404)

    print(f"📡 Producto recibido desde la API: {json.dumps(producto, indent=4, ensure_ascii=False)}")

    # Extraer detalles de inventario
    tiendas_iniciales = [item["tienda_id"] for item in producto.get("inventario", [])]

    inventario_data = producto["inventario"][0] if producto.get("inventario") else {}
    stock_inicial = inventario_data.get("stock_inicial", 0)
    cantidad_vendida = inventario_data.get("cantidad_vendida", 0)
    fecha_ultima_venta = inventario_data.get("fecha_ultima_venta", "")
    ubicacion_almacen = inventario_data.get("ubicacion_almacen", "")

    # Crear el formulario con los datos iniciales
    formulario = ProductoForm(
        datosFormulario,
        initial={
            'nombre': producto.get('nombre', ''),
            'descripcion': producto.get('descripcion', ''),
            'precio': float(producto.get('precio', 0.00)),
            'stock': producto.get('stock', 0),
            'tiendas': tiendas_iniciales,
            'stock_inicial': stock_inicial,
            'cantidad_vendida': cantidad_vendida,
            'fecha_ultima_venta': fecha_ultima_venta,
            'ubicacion_almacen': ubicacion_almacen
        }
    )

    if request.method == "POST" and formulario.is_valid():
        datos = formulario.cleaned_data.copy()
        datos["precio"] = float(datos["precio"])
        if datos["fecha_ultima_venta"]:
            datos["fecha_ultima_venta"] = datos["fecha_ultima_venta"].strftime("%Y-%m-%d")
        datos["tiendas"] = list(map(int, request.POST.getlist("tiendas")))

        resultado = actualizar_producto(producto_id, datos)

        if resultado["success"]:
            messages.success(request, "El producto ha sido actualizado correctamente.")
            return redirect("listar_productos")
        else:
            messages.error(request, resultado["message"])
            return tratar_errores(request, resultado["status"])

    return render(request, "producto/actualizar.html", {"formulario": formulario, "producto": producto})

# PATCH - Editar solo el stock disponible de un producto
def producto_editar_stock(request, producto_id):
    datosFormulario = None
    producto = obtener_producto(producto_id)  # Obtiene el producto desde la API

    if not producto:
        messages.error(request, "No se pudo obtener el producto.")
        return redirect("listar_productos")

    # Asegurar que la clave correcta está en el diccionario
    formulario = ProductoEditarStockForm(
        datosFormulario,
        initial={'stock': producto.get('stock', 0)}  # Usa el valor actual de stock
    )

    if request.method == "POST":
        formulario = ProductoEditarStockForm(request.POST)

        if formulario.is_valid():
            try:
                headers = crear_cabecera()
                datos = request.POST.copy()

                response = requests.patch(
                    f"{API_BASE_URL}productos/editar/stock/{producto_id}/",
                    headers=headers,
                    data=json.dumps(datos)
                )
                
                if response.status_code == 404:
                    return tratar_errores(request, 404)
                elif response.status_code == 500:
                    return tratar_errores(request, 500)
                
                response.raise_for_status()

                if response.status_code == 200:
                    messages.success(request, "Stock del producto actualizado correctamente.")
                    return redirect("listar_productos")
                else:
                    response.raise_for_status()

            except requests.exceptions.HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error, errores[error])
                    return render(request, 'producto/actualizar_stock.html', {"formulario": formulario, "producto": producto})
                else:
                    print(" ERROR: Ocurrió un problema en la actualización del stock del producto.")
                    print(" Enviando petición PATCH a:", f'{API_BASE_URL}productos/editar/stock/{producto_id}')

                messages.error(request, "Error al actualizar el stock del producto. Revisa la consola para más detalles.")
                return redirect("listar_productos")

    return render(request, 'producto/actualizar_stock.html', {"formulario": formulario, "producto": producto})

# DELETE Producto
def producto_eliminar(request, producto_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            f'http://127.0.0.1:8000/api/v1/productos/eliminar/{producto_id}',
            headers=headers,
        )
        
        if response.status_code == 404:
                return tratar_errores(request, 404)
        elif response.status_code == 500:
                return tratar_errores(request, 500)
            
        response.raise_for_status()
        
        if response.status_code == requests.codes.ok:
            messages.success(request, "Producto eliminado correctamente.")
        else:
            messages.error(request, "No se pudo eliminar el producto.")
    except Exception as err:
        messages.error(request, f"Ocurrió un error: {err}")

    return redirect("listar_productos")  # Redirigir siempre a la lista de productos

# Vista de registro

def registrar_usuario(request):
    if request.method == "POST":
        try:
            formulario = RegistroForm(request.POST)
            if formulario.is_valid():
                headers = {
                    "Content-Type": "application/json"
                }
                
                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/registrar/usuario/",
                    headers=headers,
                    data=json.dumps(formulario.cleaned_data)
                )
                
                if response.status_code == requests.codes.created:
                    usuario = response.json()
                    
                    # Obtener el token de sesión automáticamente después del registro
                    token_acceso = obtener_token_session(
                        formulario.cleaned_data.get("username"),
                        formulario.cleaned_data.get("password1")
                    )

                    if token_acceso:
                        headers = {"Authorization": f"Bearer {token_acceso}"}
                        response_usuario = requests.get(f"http://127.0.0.1:8000/api/v1/usuario/token/{token_acceso}/", headers=headers)

                        if response_usuario.status_code == 200:
                            usuario = response_usuario.json()
                            request.session["usuario"] = usuario
                            request.session["token"] = token_acceso
                            messages.success(request, "Registro exitoso. Bienvenido al Museo.")
                            return redirect("index")
                        else:
                            messages.error(request, "No se pudo recuperar los datos del usuario.")
                    else:
                        messages.error(request, "No se pudo obtener el token de acceso.")
                else:
                    response.raise_for_status()
        
        except HTTPError as http_err:
            print(f'Error en la petición: {http_err}')
            
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'registration/signup.html', {"formulario": formulario})
            else:
                return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f'Ocurrió un error inesperado: {err}')
            return tratar_errores(request, 500)

    else:
        formulario = RegistroForm()
    
    return render(request, 'registration/signup.html', {'formulario': formulario})


def login(request):
    if request.method == "POST":
        formulario = LoginForm(request.POST)

        if formulario.is_valid():
            try:
                username = formulario.cleaned_data.get("username")
                password = formulario.cleaned_data.get("password")

                # Obtener token de acceso desde la API
                token_acceso = obtener_token_session(username, password)
                if not token_acceso:
                    raise Exception("No se pudo obtener el token de acceso.")

                # Guardar token en la sesión
                request.session["token"] = token_acceso
                
                # Obtener información del usuario autenticado desde la API
                headers = {"Authorization": f"Bearer {token_acceso}"}
                response = requests.get(f"http://127.0.0.1:8000/api/v1/usuario/token/{token_acceso}/", headers=headers)

                if response.status_code == 200:
                    usuario = response.json()
                    request.session["usuario"] = usuario
                    request.session["user_authenticated"] = True
                    
                    # Obtener nombre y rol del usuario
                    nombre_usuario = usuario.get("username", "Usuario")
                    rol = usuario.get("rol")

                    # Definir el nombre del rol según su código
                    roles = {1: "Administrador", 2: "Visitante", 3: "Responsable"}
                    nombre_rol = roles.get(rol, "Desconocido")

                    # Mostrar mensaje de bienvenida con nombre y rol
                    messages.success(request, f"Bienvenido {nombre_usuario}, tienes el rol de {nombre_rol}.")


                    return redirect("index")

                else:
                    messages.error(request, "No se pudo recuperar los datos del usuario.")
                    return render(request, "registration/login.html", {"form": formulario})

            except Exception as excepcion:
                messages.error(request, f"Hubo un error en la autenticación: {excepcion}")
                return render(request, "registration/login.html", {"form": formulario})

    else:
        formulario = LoginForm()
    
    return render(request, "registration/login.html", {"form": formulario})


def logout(request):
    # Eliminar el token si existe en la sesión
    request.session.pop("token", None)
    request.session.pop("usuario", None)  # También eliminamos los datos del usuario

    return redirect("index")  # Redirigir al inicio



def tratar_errores(request,codigo):
    if codigo == 404:
        return mi_error_404(request)
    else:
        return mi_error_500(request)
    
#Páginas de Error
def mi_error_404(request,exception=None):
    logger.error(f"Error 404 - Página no encontrada: {request.path}")  # Log en consola
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    logger.error(f"Error 500 - Error interno del servidor en {request.path}")  # Log en consola
    return render(request, 'errores/500.html',None,None,500)