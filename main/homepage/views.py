from django.shortcuts import render
from animepage.models import Anime, AdditionalName, Film
from itertools import chain
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import JsonResponse
from django.views import View

def insertion_sort(objects):
    for i in range(1, len(objects)):
        key = objects[i]
        j = i - 1
        while j >= 0 and key.created_at > objects[j].created_at:
            objects[j + 1] = objects[j]
            j -= 1
        objects[j + 1] = key
    return objects
   #2443
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
    order_by_param = request.GET.get('order_by', 'title')
    
    
    anime = Anime.objects.all()
    films = Film.objects.all()
    combined_objects = list(chain(anime, films))
    sorted_objects = insertion_sort(combined_objects) # Сортировка никак не относится к сортировке на сайте
    
    
    if order_by_param == 'created_at':
        # Если сортировка по дате, реверсируем список
        sorted_objects = sorted(sorted_objects, key=lambda obj: getattr(obj, order_by_param), reverse=True)
    else:
        sorted_objects = sorted(sorted_objects, key=lambda obj: getattr(obj, order_by_param))
    
    paginator = Paginator(sorted_objects, 12)  # Измените на нужный размер страницы

    try:
        page_objects = paginator.page(page_number)
        
    except:
        return JsonResponse([], safe=False)
    
    ongoings = Anime.objects.filter(status='Онгоинг')[:5]
    news = Anime.objects.all().order_by("created_at").reverse()[:5]

    anime_data = [{'id': obj.id,
                   'title': obj.title,
                   'description': obj.description,
                   'image_url': obj.image.url,
                   "type": obj.temp_type,
                   "date_published": obj.temp_type,
                   } for obj in page_objects]
    ongoing_data = [{'id': obj.id, 'title': obj.title,
                     'description': obj.description,
                     'image_url': obj.image.url,
                     "type": obj.temp_type,
                     'anitype': obj.anime_type,
                     "episodes": obj.amount_of_episodes} for obj in ongoings]
    news_data = [{'id': obj.id, 'title': obj.title,
                     'description': obj.description,
                     'image_url': obj.image.url,
                     "type": obj.temp_type,
                     'anitype': obj.anime_type,
                     "episodes": obj.amount_of_episodes} for obj in news]
    
    context = {
        "anime_data": anime_data,
        "ongoing_data": ongoing_data,
        'news_data': news_data,
    }
    return JsonResponse(context, safe=False)


def registration(request):
    return render(request, "registration/registration.html")