from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('<username>/', views.user_page, name='user_page'),
]