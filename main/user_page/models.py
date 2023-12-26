from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
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
    
    
@receiver(post_save, sender=CustomUser)
def create_lists_for_new_user(sender, instance, created, **kwargs):
    if created:
        # Создаем три списка для нового пользователя
        UserList.objects.create(user=instance, name='Смотрю')
        UserList.objects.create(user=instance, name='Просмотрено')
        UserList.objects.create(user=instance, name='Запланировано')
    
class Rating(models.Model):
    anime = models.ForeignKey('animepage.Anime', on_delete=models.CASCADE, default='0')
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
    user_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.anime} - {self.author.username} - {self.id}'
    
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.comment.id} - {self.author.username} - {self.id}'
    
    
