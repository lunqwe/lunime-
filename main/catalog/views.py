from django.shortcuts import render
from animepage.models import Anime, Genre, Film
from itertools import chain

# Create your views here.
def catalog(request):
    anime = Anime.objects.all()[:5]
    genres = Genre.objects.all()[:5]
    films = Film.objects.all()[:5]
    anime_ova = Anime.objects.filter(anime_type='OVA')
    film_ova = Film.objects.filter(anime_type='OVA')
    ova_list = list(chain(anime_ova,film_ova))[:5]
    anime_ona = Anime.objects.filter(anime_type='ONA')
    film_ona = Film.objects.filter(anime_type='ONA')
    ona_list = list(chain(anime_ona, film_ona))[:5]
    anime_special = Anime.objects.filter(anime_type='Спешл')
    film_special = Film.objects.filter(anime_type='Спешл')
    specials_list = list(chain(anime_special, film_special))[:5]
    
    context = {
        "anime_list": anime,
        "films": films,
        'genres': genres,
        "ova_list": ova_list,
        "ona_list": ona_list,
        "specials_list": specials_list,
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