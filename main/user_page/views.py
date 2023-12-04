from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth import login


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

@login_required(login_url='/login')
def user_page(request):
    return render(request, 'user/user_page.html')