from django.urls import path, re_path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('museos/',views.listar_museos, name='listar_museos'),
    path('museos/buscar_simple/', views.museo_buscar_simple, name='museo_buscar_simple'),
    path('museo/create/',views.museo_create, name='museo_create'),
    path('museo/editar/<int:museo_id>/', views.museo_editar, name='museo_editar'),
    path('museo/editar/nombre/<int:museo_id>/', views.museo_editar_nombre, name='museo_editar_nombre'),
    path('museos/busqueda_avanzada/', views.museo_buscar_avanzada, name='museo_buscar_avanzada'),
    path('museo/eliminar/<int:museo_id>/', views.museo_eliminar, name='museo_eliminar'),
    
    path('obras/', views.listar_obras, name='listar_obras'),
    path('obras/busqueda_avanzada/', views.obra_buscar_avanzada, name='obra_buscar_avanzada'),
    
    path('exposiciones/', views.listar_exposiciones, name='listar_exposiciones'),
    path('expocisiones/busqueda_avanzada/', views.exposicion_buscar_avanzada, name='exposicion_buscar_avanzada'),
    
    path('entradas/', views.listar_entradas, name='listar_entradas'),
    path('entradas/busqueda_avanzada/', views.entrada_buscar_avanzada, name='entrada_buscar_avanzada'),
]