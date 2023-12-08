from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone

    
class Genre(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='genres/', default='images/default.png')
    
    def __str__(self):
        return self.name
    
    
class Film(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField()
    anime_type = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre)
    origin_source = models.CharField(max_length=255)
    description = models.CharField(max_length=1500)
    duration = models.CharField(max_length=255)
    date_published = models.CharField(max_length=255)
    studio = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    temp_type = models.CharField(max_length=255, default = 'Film')
    anilibria_player = models.CharField(max_length=225, default=0)
    
    def __str__(self):
        return self.title
    
    
class Anime(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="anime_covers/")
    anime_type = models.CharField(max_length=255, default="ТВ-Сериал")
    description = models.CharField(max_length=1500)
    date_published = models.CharField(max_length=255)
    status = models.CharField(max_length=100, default="Онгоинг")
    created_at = models.DateTimeField(auto_now_add=True)
    studio = models.CharField(max_length=255, default='0')
    amount_of_episodes = models.CharField(max_length = 255, default=0)
    genres = models.ManyToManyField(Genre)
    anilibria_link = models.CharField(max_length=999, default=0)
    duration = models.CharField(max_length=255, default=0)
    origin_source = models.CharField(max_length=255, default=0)
    temp_type = models.CharField(max_length=255, default = 'Anime') 
    def __str__(self):
        return self.title

class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, default="1")
    n_episode = models.IntegerField(default=1)
    kodik_link = models.CharField(max_length=999, default=0)
    
    def __str__(self):
        return f"{self.anime.title} - {self.n_episode}" 

class AdditionalImage(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, default="/")
    image = models.ImageField(upload_to="additional_images/")

class AdditionalName(models.Model):
    title_name = models.CharField(max_length=255)
    title = models.ForeignKey(Anime, on_delete=models.CASCADE)