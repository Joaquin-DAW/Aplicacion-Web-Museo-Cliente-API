from django.shortcuts import render,redirect
import requests

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    return render(request, 'index.html')

def listar_museos(request):
    #Obtenemos todos los museos
    headers = {'Authorization': 'Bearer Tptiypl35obv48FlzLegD6dscLrvBC'} 
    response = requests.get('http://127.0.0.1:8000/api/v1/museos', headers=headers)
    #Transformamos la respuesta en json
    museos = response.json()
    
    return render(request, 'estructura/museo/lista.html',{"museos":museos})

def listar_obras(request):
    headers = {'Authorization': 'Bearer Tptiypl35obv48FlzLegD6dscLrvBC'} 
    response = requests.get('http://127.0.0.1:8000/api/v1/obras', headers=headers)
    obras = response.json()
    
    return render(request, 'estructura/obra/lista.html', {'obras': obras})