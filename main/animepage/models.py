from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from user_page.models import CustomUser
    
class Genre(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='genres/', default='images/default.png')
    
    def __str__(self):
        return self.name
    
class Anime(models.Model):
    title = models.CharField(max_length=255, default=0)
    original_title = models.CharField(max_length=255, default=0)
    anime_type = models.CharField(max_length=255, default='ТВ-Серіал')
    amount_of_episodes = models.CharField(max_length=255, default=0)
    description = models.TextField(max_length=999, default=0)
    date_published = models.CharField(max_length=255, default=0)
    studio = models.CharField(max_length=255, default=0)
    cover = models.ImageField(default='images/default.png')
    player = models.CharField(max_length=500, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField(Genre)
    temp_type = models.CharField(max_length=255, default='Anime')
    
    def __str__(self):
        return self.title


class AdditionalImage(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="additional_images/")
    
    def __str__(self):
        return self.anime.title

    
    