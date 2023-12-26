from django.shortcuts import render
from animepage.models import Anime, Genre
from itertools import chain

# Create your views here.
def catalog(request):
    anime = Anime.objects.all()[:5]
    genres = Genre.objects.all()[:5]
    anime_ova = Anime.objects.filter(anime_type='OVA')
    anime_ona = Anime.objects.filter(anime_type='ONA')
    anime_special = Anime.objects.filter(anime_type='Спешл')
    
    context = {
        "anime_list": anime,
        'genres': genres,
    }
    
    
    return render(request, "catalog/catalog.html", context)

def genres(request):
    genres = Genre.objects.all().order_by('name')
    return render(request, "catalog/genres.html", {"genres" : genres})

def seasons(request):
    return render(request, 'catalog/seasons.html')

def get_genre(request, pk):
    genre = Genre.objects.filter(id=pk)[0]
    anime_list = Anime.objects.filter(genres=genre)
    print(genre.name)
    return render(request, 'catalog/genre.html', {"genre" : genre, 'anime_list': anime_list})