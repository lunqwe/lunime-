from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.main, name='homepage'),
    path('get_anime/', views.get_anime, name='get_anime'),
    path('search-results/', views.search_result, name='search_suggestions'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
]
