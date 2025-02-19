from django.urls import path, re_path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('museos/',views.listar_museos, name='listar_museos'),
    path('obras/', views.listar_obras, name='listar_obras'),
    path('exposiciones/', views.listar_exposiciones, name='listar_exposiciones'),
    path('entradas/', views.listar_entradas, name='listar_entradas'),
    
    path('museos/buscar_simple/', views.museo_buscar_simple, name='museo_buscar_simple'),
    path('museos/busqueda_avanzada/', views.museo_buscar_avanzada, name='museo_buscar_avanzada'),
    
    path('obras/busqueda_avanzada/', views.obra_buscar_avanzada, name='obra_buscar_avanzada'),
    
    path('expocisiones/busqueda_avanzada/', views.exposicion_buscar_avanzada, name='exposicion_buscar_avanzada'),
    
    path('entradas/busqueda_avanzada/', views.entrada_buscar_avanzada, name='entrada_buscar_avanzada'),
]
