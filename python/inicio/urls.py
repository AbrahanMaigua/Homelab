# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("",                home, name="home"),
    path('doc/',            lista_articulos, name='lista_articulo'),
    path("dashboard/",      dashboard, name="dashboard"),
    path('editor/',         editor_view, name='editor'),
    # post
    path('rule/',           rule, name='rule'),
    path('api/posts/create',create_post, name='create_post'),
    path('api/posts/',      post_list, name='post_list'),
    path('api/posts/<int:pk>/', post_detail, name='post_detail'),
]
