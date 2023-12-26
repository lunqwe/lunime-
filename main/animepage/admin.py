from django.contrib import admin
from .models import Genre, Anime, AdditionalImage
# Register your models here.
admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(AdditionalImage)