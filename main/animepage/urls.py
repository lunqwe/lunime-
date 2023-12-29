from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('<int:pk>/', views.get_anime, name='anime'),
    path('', views.anime_view, name='home'),
]