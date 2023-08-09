from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView
import requests
from bs4 import BeautifulSoup


class MainPage(ListView):
    """Класс представления главной страницы"""

    def get(self, request, *args, **kwargs):
        """Обработка get-запроса"""
        user_data = SocialAccount.objects.filter(user=request.user)
        context = {}

        if user_data:
            user_data = user_data[0]

            user_steam_id = user_data.extra_data.get('steamid')

            # Получение данных FaceIT по Steam ID
            request_for_faceit_data = 'https://api.faceit.com/search/v1/?limit=3&query=' + user_steam_id
            faceit_user_data = requests.get(request_for_faceit_data).json().get('payload').get('players').get('results')

            if faceit_user_data:
                faceit_user_data = faceit_user_data[0]
                context['faceit_user_data'] = faceit_user_data

        return render(request, 'main/main.html', context)


class ProfilePage(DetailView):
    """Класс представления страницы профиля пользователя"""
    model = SocialAccount
    template_name = 'main/profile.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        """Обработка get-запроса"""
        user_data = SocialAccount.objects.filter(user=request.user)
        context = {}

        # Проверка на то, является ли пользователь админом
        if user_data:
            user_data = user_data[0]

            user_steam_id = user_data.extra_data.get('steamid')

            # Получение данных FaceIT по Steam ID
            request_for_faceit_data = 'https://api.faceit.com/search/v1/?limit=3&query=' + user_steam_id
            faceit_user_data = requests.get(request_for_faceit_data).json().get('payload').get('players').get('results')

            if faceit_user_data:
                faceit_user_data = faceit_user_data[0]
                context['faceit_user_data'] = faceit_user_data

        else:
            user_data = {
                'extra_data': {
                    'avatarfull': '',
                    'personaname': request.user,
                    'profileurl': '',
                }
            }

        context['user_data'] = user_data
        return render(request, 'main/profile.html', context)
