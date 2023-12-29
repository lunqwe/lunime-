from django.shortcuts import render
from animepage.models import Anime, Genre
from itertools import chain
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt


def insertion_sort(objects, selected_genres=None):
    for i in range(1, len(objects)):
        key = objects[i]
        j = i - 1
        while j >= 0 and key.created_at > objects[j].created_at:
            objects[j + 1] = objects[j]
            j -= 1
        objects[j + 1] = key
        
    if selected_genres:
        objects = [obj for obj in objects if any(genre.id in selected_genres for genre in obj.genres.all())]

    return objects
   #2443
# Create your views here.
def main(request):
    anime = Anime.objects.all()
    combined_objects = list(anime)
    sorted_objects = insertion_sort(combined_objects)
    novelty_list = sorted_objects[:4]
    genres = Genre.objects.all()
        
    return render(request, "homepage/main.html", {'anime_list' : sorted_objects, 'novelty_list' : novelty_list, 'genres': genres})

def get_anime(request):
    page_number = request.GET.get('page', 0)
    order_by_param = request.GET.get('order_by', 'title')
    selected_genres = request.GET.getlist('selectedGenres[]', [])
    selected_types = request.GET.getlist('selectedTypes[]', []) # получения значений фильтрации типов
    
    if selected_genres:
        anime = Anime.objects.filter(genres__id__in=selected_genres).annotate(genre_count=Count('genres')).filter(genre_count=len(selected_genres))
    else:
        anime = Anime.objects.all()
    
    if selected_types:
        print(selected_types)
        anime = anime.filter(anime_type__in=selected_types)
        sorted_objects = anime
    else:
        sorted_objects = Anime.objects.all()

    if order_by_param == 'created_at':
        sorted_objects = sorted(sorted_objects, key=lambda obj: getattr(obj, order_by_param), reverse=True)
    else:
        sorted_objects = sorted(sorted_objects, key=lambda obj: getattr(obj, order_by_param))

    
    paginator = Paginator(sorted_objects, 12)  # Измените на нужный размер страницы
    try:
        page_objects = paginator.page(page_number)
    except:
        return JsonResponse([], safe=False)
    
    ongoings = Anime.objects.filter(anime_type='Онґоїнґ')[:5]
    news = Anime.objects.all().order_by("created_at").reverse()[:5]

    anime_data = [{'id': obj.id,
                   'title': obj.title,
                   'description': obj.description,
                   'image_url': obj.cover.url,
                   "type": obj.temp_type,
                   "date_published": obj.temp_type,
                   } for obj in page_objects]
    ongoing_data = [{'id': obj.id, 'title': obj.title,
                     'description': obj.description,
                     'image_url': obj.cover.url,
                     "type": obj.temp_type,
                     'anitype': obj.anime_type,
                     "episodes": obj.amount_of_episodes} for obj in ongoings]
    news_data = [{'id': obj.id, 'title': obj.title,
                     'description': obj.description,
                     'image_url': obj.cover.url,
                     "type": obj.temp_type,
                     'anitype': obj.anime_type,
                     "episodes": obj.amount_of_episodes} for obj in news]
    
    context = {
        "anime_data": anime_data,
        "ongoing_data": ongoing_data,
        'news_data': news_data,
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def search_suggestions(request):
    query = request.GET.get('q', '')

    print(f"Received search query: {query}")

    anime_results = Anime.objects.filter(title__icontains=query)

    suggestions = []
    for anime in anime_results:
        suggestion = {
            'id': anime.id,
            'title': anime.title,
            'type': anime.anime_type,
            'image_url': anime.cover.url,
            'check_type': anime.temp_type
        }
        suggestions.append(suggestion)
    
        
    print(f"Returning suggestions: {suggestions}")

    return JsonResponse({'suggestions': suggestions})

def search_result(request):
    query = request.GET.get('q', '')
    anime_results = Anime.objects.filter(title__icontains=query)
    
    context = {
        'query': query,
        'results': anime_results,
    }

    return render(request, 'catalog/search-result.html', context)

def registration(request):
    return render(request, "registration/registration.html")