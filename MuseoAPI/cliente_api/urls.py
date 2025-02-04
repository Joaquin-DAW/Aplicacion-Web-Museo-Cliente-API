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
]
