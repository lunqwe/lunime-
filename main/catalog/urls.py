from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('genres/', views.genres, name='genres'),
    path('genre/<int:pk>/', views.genre, name='genre'),
    path('get_genre/', views.get_genre, name='get_genre'),
    path('type/<str:a_type>', views.type_view, name='type_view'),
    path('get_type/', views.get_type, name='get_type'),
]