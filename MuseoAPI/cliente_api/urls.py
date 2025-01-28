from django.urls import path, re_path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('museos/',views.listar_museos, name='listar_museos'),
]
