from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    profile_description = models.CharField(max_length=350, default="0")
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default_pfpic.png')
    


