from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class CustomUser(AbstractUser):
    profile_description = models.CharField(max_length=350, default="Описание отсутствует")
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default_pfpic.png')
    
    def __str__(self):
        return f'{self.id} - {self.username}'
    

class UserList(models.Model):
    name = models.CharField(max_length=350, default='Неопознаный список')
    anime = models.ManyToManyField("animepage.Anime", blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username} - "{self.name}"'
    
class Rating(models.Model):
    anime = models.ForeignKey('animepage.Anime', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mark = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    


class Selection(models.Model):
    name = models.CharField(max_length=350)
    description = models.CharField(max_length=999)
    image = models.ImageField(default='default_pfpic.png')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    anime = models.ManyToManyField('animepage.Anime')
    
    def __str__(self):
        return f'{self.user.username} - {self.name}'
    
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    anime = models.ForeignKey('animepage.Anime', on_delete=models.CASCADE, null=True, blank=True)
    film = models.ForeignKey('animepage.Film', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.anime} - {self.user.username} - {self.id}'

