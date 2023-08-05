from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView


class MainPage(ListView):
    """Класс представления главной страницы"""

    def get(self, request, *args, **kwargs):
        """Обработка get-запроса"""

        context = {}

        return render(request, 'main/main.html', context)


class ProfilePage(DetailView):
    """Класс представления страницы профиля пользователя"""
    model = SocialAccount
    template_name = 'main/profile.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        """Обработка get-запроса"""
        user_data = SocialAccount.objects.filter(user=request.user)

        # Проверка на то, является ли пользователь админом
        if user_data:
            user_data = user_data[0]
        else:
            user_data = {
                'extra_data': {
                    'avatarfull': '',
                    'personaname': request.user,
                    'profileurl': '',
                }
            }
        context = {'user_data': user_data}
        return render(request, 'main/profile.html', context)

