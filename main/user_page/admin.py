from django.contrib import admin
from .models import CustomUser, UserList, Rating
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserList)
admin.site.register(Rating)