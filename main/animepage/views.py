from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Anime, Genre, AdditionalImage
from .services import open_file
from user_page.models import UserList, Comment 


def get_list_video(request):
    return render(request, 'catalog/catalog.html')


def get_anime(request, pk: int):
    anime = get_object_or_404(Anime, id=pk)
    additional_images = AdditionalImage.objects.filter(anime=anime)
    if request.user.is_anonymous:
        user_lists = []
    else: 
        user_lists = UserList.objects.filter(user=request.user)
    
    comments = Comment.objects.filter(anime=anime).order_by('date_created').reverse()
    
    context = {
        "anime": anime,
        "additional_images": additional_images,
        "user_lists": user_lists,
        "comments": comments,
    }
    
    return render(request, "animepage/anime.html", context)


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response