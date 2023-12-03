from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('genres/', views.genres, name='genres'),
    path('seasons/', views.seasons, name='seasons'),
    path('genre/<int:pk>/', views.get_genre, name='video'),
]