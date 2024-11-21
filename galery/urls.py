from django.urls import path
from . import views

urlpatterns = [
    path('cargar/', views.cargar_imagen, name='cargar_imagen'),
    path('imagenes/', views.lista_imagenes, name='lista_imagenes'),
]
