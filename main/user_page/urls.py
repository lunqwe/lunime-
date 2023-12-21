from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('<username>/', views.user_page, name='user_page'),
    path('<username>/list/', views.lists, name='lists'),
    path('delete_from_list/<int:list_id>/<int:anime_id>/', views.delete_from_list, name='delete_from_list'),
    path('add_to_list/<int:list_id>/<int:anime_id>/', views.add_to_list, name='add_to_list'),
    path('<username>/change-profile/', views.change_profile, name='change-profile'),
    path('change-nickname/<str:new_name>/', views.change_nickname, name='change_nickname'),
]