import requests
from django.shortcuts import render,redirect
from .forms import *
from django.conf import settings

import requests
import environ
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

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
    response = requests.get('http://127.0.0.1:8000/api/v1/museos', headers=headers)
    #Transformamos la respuesta en json
    museos = response.json()
    
    return render(request, 'museo/lista.html',{"museos":museos})

def listar_obras(request):
    headers = crear_cabecera() 
    response = requests.get('http://127.0.0.1:8000/api/v1/obras', headers=headers)
    obras = response.json()
    
    return render(request, 'obra/lista.html', {'obras': obras})

def listar_exposiciones(request):
    headers = crear_cabecera() 
    response = requests.get('http://127.0.0.1:8000/api/v1/exposiciones', headers=headers)
    exposiciones = response.json()
    
    return render(request, 'exposicion/lista.html', {'exposiciones': exposiciones})

def listar_artistas(request):
    headers = crear_cabecera() 
    response = requests.get('http://127.0.0.1:8000/api/v1/artistas', headers=headers)
    artistas = response.json()
    
    return render(request, 'estructura/artista/lista.html', {'artistas': artistas})

def listar_entradas(request):
    headers = crear_cabecera() 
    response = requests.get('http://127.0.0.1:8000/api/v1/entradas', headers=headers)
    entradas = response.json()
    
    return render(request, 'entrada/lista.html', {'entradas': entradas})

def museo_buscar_simple(request):
    if request.GET:
        formulario = BusquedaMuseoForm(request.GET)
        if formulario.is_valid():
            texto = formulario.cleaned_data.get("textoBusqueda")

            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/museos/busqueda_simple',
                headers=headers,
                params={'textoBusqueda': texto}
            )

            museos = response.json()
        
            return render(request, 'museo/lista_busqueda.html', {"museos": museos})
        else:
            return render(request, 'museo/busqueda_simple.html', {"formulario": formulario})
    
    formulario = BusquedaMuseoForm()
    return render(request, 'museo/busqueda_simple.html', {"formulario": formulario})


def museo_buscar_avanzada(request):
    if request.GET:
        formulario = BusquedaAvanzadaMuseoForm(request.GET)

        if formulario.is_valid():
            try:
                headers = crear_cabecera()
                response = requests.get(
                    'http://127.0.0.1:8000/api/v1/museos/busqueda_avanzada/',
                    headers=headers,
                    params=formulario.cleaned_data
                )

                if response.status_code == 200:
                    museos = response.json()
                    return render(request, 'museo/lista_busqueda.html', {"museos": museos, "formulario": formulario})
                
                elif response.status_code == 400:
                    errores = response.json()  # Captura los errores del servidor
                    return render(request, 'museo/busqueda_avanzada.html', {"formulario": formulario, "errores": errores})

            except Exception as err:
                return render(request, 'museo/busqueda_avanzada.html', {"formulario": formulario, "error": str(err)})
    
    formulario = BusquedaAvanzadaMuseoForm()
    return render(request, 'museo/busqueda_avanzada.html', {"formulario": formulario})
