from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from animepage.models import Anime, AdditionalName, Film
from django.utils import timezone
from itertools import chain
from operator import attrgetter
from user_page.models import CustomUser
from user_page.forms import CustomUserCreationForm


def insertion_sort(objects):
    for i in range(1, len(objects)):
        key = objects[i]
        j = i - 1
        while j >= 0 and key.created_at > objects[j].created_at:
            objects[j + 1] = objects[j]
            j -= 1
        objects[j + 1] = key
    return objects
   
# Create your views here.
def main(request):
    anime = Anime.objects.all()
    films = Film.objects.all()
    combined_objects = list(chain(anime, films))
    sorted_objects = insertion_sort(combined_objects)
    novelty_list = sorted_objects[:4]
    return render(request, "homepage/main.html", {'anime_list' : sorted_objects, 'novelty_list' : novelty_list})

def registration(request):
    return render(request, "registration/registration.html")