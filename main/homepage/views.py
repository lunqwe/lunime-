from django.shortcuts import render
from animepage.models import Anime, AdditionalName, Film
from itertools import chain
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json


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

def get_anime(request):
    page_number = request.GET.get('page', 0)
    anime = Anime.objects.all()
    films = Film.objects.all()
    combined_objects = list(chain(anime, films))
    sorted_objects = insertion_sort(combined_objects)

    paginator = Paginator(sorted_objects, 12)  # Измените на нужный размер страницы

    try:
        page_objects = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse([], safe=False)

    anime_data = [{'id': obj.id, 'title': obj.title, 'description': obj.description, 'image_url': obj.image.url} for obj in page_objects]

    return JsonResponse(anime_data, safe=False)

def registration(request):
    return render(request, "registration/registration.html")