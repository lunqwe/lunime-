from django.contrib import admin
from .models import CustomUser, UserList, Rating, Comment, Reply
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserList)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Reply)