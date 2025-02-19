import requests
from django.shortcuts import render, redirect
from .forms import *
import xml.etree.ElementTree as ET #Importamos la librería para trabajar con XML
from django.contrib import messages
import json

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
    museos = tipo_respuesta(response)
    
    if "error" in museos:
        return render(request, 'museo/lista.html', {"error": museos["error"]})
    
    return render(request, 'museo/lista.html',{"museos":museos})

def listar_obras(request):
    headers = crear_cabecera() 
    response = requests.get(f'{API_BASE_URL}obras', headers=headers)
    obras = tipo_respuesta(response)
    
    if "error" in obras:
        return render(request, 'museo/lista.html', {"error": obras["error"]})
    
    return render(request, 'obra/lista.html', {'obras': obras})

def listar_exposiciones(request):
    headers = crear_cabecera() 
    response = requests.get(f'{API_BASE_URL}exposiciones', headers=headers)
    exposiciones = tipo_respuesta(response)
    
    if "error" in exposiciones:
        return render(request, 'museo/lista.html', {"error": exposiciones["error"]})
    
    return render(request, 'exposicion/lista.html', {'exposiciones': exposiciones})

def listar_artistas(request):
    headers = crear_cabecera() 
    response = requests.get(f'{API_BASE_URL}artistas', headers=headers)
    artistas = tipo_respuesta(response)
    
    if "error" in artistas:
        return render(request, 'museo/lista.html', {"error": artistas["error"]})
    
    return render(request, 'estructura/artista/lista.html', {'artistas': artistas})

def listar_entradas(request):
    headers = crear_cabecera() 
    response = requests.get(f'{API_BASE_URL}entradas', headers=headers)
    entradas = tipo_respuesta(response)
    
    if "error" in entradas:
        return render(request, 'museo/lista.html', {"error": entradas["error"]})
    
    return render(request, 'entrada/lista.html', {'entradas': entradas})

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
                
                headers = crear_cabecera()  # Incluir la cabecera con el token de autenticación

                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/museos/crear",
                    headers=headers,  # Usamos la cabecera aquí
                    data=json.dumps(datos)
                )
                
                if response.status_code == 201:
                    messages.success(request, "El museo se ha creado correctamente.")
                    return redirect("listar_museos")
                else:
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error, errores[error])
            except requests.exceptions.RequestException as e:
                messages.error(request, "Error de conexión con la API.")
            except Exception as err:
                messages.error(request, f"Ocurrió un error: {err}")
    else:
        formulario = MuseoForm()
    
    return render(request, "museo/create.html", {"formulario": formulario})


# PUT - Editar un museo
def museo_editar(request, museo_id):
    headers = crear_cabecera() 
    
    # Obtener el museo desde la API con autenticación
    response = requests.get(f"http://127.0.0.1:8000/api/v1/museos/{museo_id}", headers=headers)
    
    if response.status_code == 401:
        messages.error(request, "No tienes permisos para acceder a este museo. Inicia sesión nuevamente.")
        return redirect("listar_museos")

    if response.status_code != 200:
        messages.error(request, f"Error al obtener el museo desde la API (Código {response.status_code}).")
        return redirect("listar_museos")
 
    museo = response.json() 

    if request.method == "POST":
        formulario = MuseoForm(request.POST)
        if formulario.is_valid():
            try:
                datos = formulario.cleaned_data.copy()
                datos["fecha_fundacion"] = datos["fecha_fundacion"].strftime("%Y-%m-%d")
                
                print("Cabecera enviada en PUT:", headers)  # Verificar token en PUT

                response = requests.put(
                    f"http://127.0.0.1:8000/api/v1/museos/{museo_id}/editar",
                    headers=headers,
                    data=json.dumps(datos)
                )
                
                if response.status_code == 200:
                    messages.success(request, "El museo se ha actualizado correctamente.")
                    return redirect("listar_museos")
                elif response.status_code == 401:
                    messages.error(request, "No tienes permisos para actualizar este museo.")
                    return redirect("listar_museos")
                else:
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error, errores[error])
            except requests.exceptions.RequestException as e:
                messages.error(request, "Error de conexión con la API.")
            except Exception as err:
                messages.error(request, f"Ocurrió un error: {err}")
    else:
        formulario = MuseoForm(initial={
            'nombre': museo['nombre'],
            'ubicacion': museo['ubicacion'],
            'fecha_fundacion': museo['fecha_fundacion'],
            'descripcion': museo['descripcion']
        })
    
    return render(request, "museo/actualizar.html", {"formulario": formulario, "museo": museo})


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