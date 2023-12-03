from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('<int:pk>/', views.get_anime, name='anime'),
    path('film/<int:pk>/', views.get_film, name='film'),
    path('', views.get_list_video, name='home'),
]