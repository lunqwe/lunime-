from django.shortcuts import render
from animepage.models import Anime, Genre

# Create your views here.
def catalog(request):
    anime = Anime.objects.all()
    genres = Genre.objects.all()[:5]
    return render(request, "catalog/catalog.html", {"anime_list": anime, "genres": genres})

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