from django.contrib import admin
from .models import Genre, Anime, Episode, AdditionalName, Film
# Register your models here.
admin.site.register(Genre)
admin.site.register(Anime)
admin.site.register(Episode)
admin.site.register(AdditionalName)
admin.site.register(Film)