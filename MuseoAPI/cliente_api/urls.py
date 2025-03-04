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
    path('exposicion/crear/', views.exposicion_create, name='exposicion_create'),
    path('exposiciones/editar/<int:exposicion_id>/', views.exposiciones_editar, name='exposiciones_editar'),
    path('exposicion/editar/capacidad/<int:exposicion_id>/', views.exposicion_editar_capacidad, name='exposicion_editar_capacidad'),
    path('exposicion/eliminar/<int:exposicion_id>/', views.exposicion_eliminar, name='exposicion_eliminar'),
    
    path('entradas/', views.listar_entradas, name='listar_entradas'),
    path('entradas/busqueda_avanzada/', views.entrada_buscar_avanzada, name='entrada_buscar_avanzada'),
    
    path('visitasguiadas/', views.listar_visitas_guiadas, name='listar_visitas_guiadas'),
    path('visitasguiadas/crear/', views.visita_guiada_create, name='visita_guiada_create'),
    path('visitasguiadas/editar/<int:visita_id>/', views.visita_guiada_editar, name='visita_guiada_editar'),
    path('visitasguiadas/editar/capacidad/<int:visita_id>/', views.visita_guiada_editar_capacidad, name='visita_guiada_editar_capacidad'),
    path('visitasguiadas/eliminar/<int:visita_id>/', views.visita_guiada_eliminar, name='visita_guiada_eliminar'),
    
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.producto_create, name='producto_create'),
    path('productos/editar/<int:producto_id>/', views.producto_editar, name='producto_editar'),
    path('productos/editar/stock/<int:producto_id>/', views.producto_editar_stock, name='producto_editar_stock'),
    path('productos/eliminar/<int:producto_id>/', views.producto_eliminar, name='producto_eliminar'),
    
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', views.login, name='login'),
    path('logout',views.logout,name='logout'),
]