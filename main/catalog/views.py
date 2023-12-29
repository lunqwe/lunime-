from django.shortcuts import render
from animepage.models import Anime, Genre
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
def catalog(request):
    anime = Anime.objects.all()[:5]
    genres = Genre.objects.all()[:5]
    films = Anime.objects.filter(anime_type='Фільм')[:5]
    ova = Anime.objects.filter(anime_type='OVA')[:5]
    ona = Anime.objects.filter(anime_type='ONA')[:5]
    
    context = {
        "anime_list": anime,
        'genres': genres,
        "films": films,
        "ova_list": ova,
        "ona_list": ona
    }
    
    
    return render(request, "catalog/catalog.html", context)

def genres(request):
    genres = Genre.objects.all().order_by('name')

    return render(request, "catalog/genres.html", {"genres" : genres})

def genre(request, pk):
    genre = Genre.objects.filter(id=pk)[0]
    print(genre)
    
    return render(request, 'catalog/genre.html', context={"genre":genre})

def get_genre(request):
    page_number = request.GET.get('page', 0)
    genre = request.GET.get('genre', 0)
    anime_list = Anime.objects.filter(genres=genre)
    
    paginator = Paginator(anime_list, 12)  # Измените на нужный размер страницы
    try:
        page_objects = paginator.page(page_number)
    except:
        return JsonResponse([], safe=False)
    
    anime_data = [{'id': obj.id,
                   'title': obj.title,
                   'description': obj.description,
                   'image_url': obj.cover.url,
                   "type": obj.temp_type,
                   "date_published": obj.temp_type,
                   } for obj in page_objects]
    
    context = {
        "anime_data": anime_data,
    }
    return JsonResponse(context, safe=False)

def type_view(request, a_type):
    
    temp_type_changer = {
        'anime': "Аніме",
        'film': "Фільми",
        'ova': "OVA",
        'ona': "ONA",
    }
    context = {
        "anime_type": a_type,
        "display_type": temp_type_changer[a_type],
    }
    return render(request, 'catalog/type_anime.html', context)


def get_type(request):
    page_number = request.GET.get('page', 0)
    a_type = request.GET.get('typeChosen', 0)
    
    type_changer = {
        'anime': "ТВ-Серіал",
        'film': "Фільм",
        'ova': "OVA",
        'ona': "ONA",
    }
    
    if a_type == 'Добірки':
        pass
    else:
        anime_list = Anime.objects.filter(anime_type=type_changer[a_type]).order_by('title')
        
    paginator = Paginator(anime_list, 12)  # Измените на нужный размер страницы
    try:
        page_objects = paginator.page(page_number)
    except:
        return JsonResponse([], safe=False)
    
    anime_data = [{'id': obj.id,
                   'title': obj.title,
                   'description': obj.description,
                   'image_url': obj.cover.url,
                   "type": obj.temp_type,
                   "date_published": obj.temp_type,
                   } for obj in page_objects]
    
    context = {
        "anime_data": anime_data,
    }
    return JsonResponse(context, safe=False)