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
    path('change-description/<str:new_description>/', views.change_description, name='change_description'),
    path('change_profile_picture/', views.change_profile_picture, name='change_profile_picture'),
    path('create_comment/<str:comment_type>/<int:object_id>/<str:text>/', views.create_comment, name='create_comment'),
    path('create_reply/<str:text>/<int:comment_id>', views.create_reply, name='create_reply'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('delete_reply/<int:reply_id>', views.delete_reply, name='delete_reply')
]