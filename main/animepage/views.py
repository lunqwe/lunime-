
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Anime, Episode, AdditionalName, Genre, Film, AdditionalImage, AdditionalFilmImage
from .services import open_file


def get_list_video(request):
    return render(request, 'catalog/catalog.html', {'video_list': Episode.objects.all()})


def get_anime(request, pk: int):
    anime = get_object_or_404(Anime, id=pk)
    episodes = Episode.objects.filter(anime=anime).order_by("n_episode")
    kodik_link = episodes[0]
    additional_names = AdditionalName.objects.filter(anime=anime)
    additional_images = AdditionalImage.objects.filter(anime=anime)
    
    
    context = {
        "anime": anime,
        "episodes": episodes,
        "link": kodik_link,
        "additional_names": additional_names,
        "additional_images": additional_images,
    }
    
    return render(request, "animepage/anime.html", context)

def get_film(request, pk: int):
    film = get_object_or_404(Film, id=pk)
    kodik_link = film.link
    additional_images = AdditionalFilmImage.objects.filter(film=film)
    
    print(film.genres.all())
    
    context = {
        "film": film,
        "link": kodik_link,
        "additional_images": additional_images,
    }
    
    return render(request, "animepage/film.html", context)


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response