# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("interface/",      consola_page, name="consola_page"),
    path("consola/",        consola, name="consola"),
]
