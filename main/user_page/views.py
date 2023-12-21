from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, ChangeUsernameForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth import login
from animepage.models import Anime, Film
from .models import CustomUser, UserList, Selection
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
class SignupView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('homepage:main')
    template_name = 'registration/registration.html'
    
    def form_valid(self, form):
        # Проверка уникальности имени пользователя
        username = form.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            form.add_error('username', 'Пользователь с таким именем уже зарегистрирован.')
            return self.form_invalid(form)

        # Проверка уникальности почтового адреса
        email = form.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            form.add_error('email', 'Пользователь с такой почтой уже зарегистрирован.')
            return self.form_invalid(form)

        # Если все проверки прошли успешно, сохраняем форму
        response = super().form_valid(form)
        
        login(self.request, self.object)
        # Добавьте следующую строку для редиректа
        return redirect(self.success_url)

def user_page(request, username):
    # Получаем объект пользователя по его имени пользователя
    user = get_object_or_404(CustomUser, username=username)

    # Загружаем данные для профиля пользователя
    anime = Anime.objects.all()[:5]
    films = Film.objects.all()[:3]
    
    context = {
        "profile_owner": user,  # Предположим, что у пользователя есть модель профиля
        "anime_list": anime,
        "film_list": films,
    }

    return render(request, 'user/user_page.html', context)

def lists(request, username):
    user = get_object_or_404(CustomUser, username=username)
    
    lists = UserList.objects.filter(user=user)
    
    context = {
        "lists_owner": user,
        "lists": lists
    }
    
    return render(request, 'user/lists.html', context)



@require_POST
def delete_from_list(request, list_id, anime_id):
    user = request.user
    user_list = UserList.objects.get(user=user, id=list_id)
    anime = Anime.objects.get(id=anime_id)
        
    user_list.anime.remove(anime)
        
    return JsonResponse({'message': 'Аниме удалено из списка!'})


@require_POST
def add_to_list(request, list_id, anime_id):
    
    user = request.user
    user_list = UserList.objects.get(user=user, id=list_id)
    anime = Anime.objects.get(id=anime_id)
        
    user_list.anime.add(anime)
    
    return JsonResponse({'message': 'Аниме успешно добавлено в список!'})
    
@login_required
def change_profile(request, username):
    user = request.user
    
    selection = Selection.objects.filter(user=user)
    
    context = {
        "selection" : selection,
    }
    
    return render(request, 'user/change_profile.html', context)


@require_POST
def change_nickname(request, new_name):
    user = request.user
    try:
        # Попытка установить новый никнейм
        user.username = new_name
        user.save()
        return JsonResponse({'message': 'Имя пользователя успешно изменено!'})
    except IntegrityError:
        return JsonResponse({'message': 'Имя пользователя занято.', 'type': 'error'})