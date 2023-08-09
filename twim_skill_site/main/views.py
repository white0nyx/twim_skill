from allauth.socialaccount.models import SocialAccount
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
import requests


def get_all_user_data(request: WSGIRequest):
    """Формирование всех данных пользователя"""

    steam_user_data = None
    faceit_user_data = None

    if request.user.is_authenticated and not request.user.is_superuser:

        # Получение данных Steam
        steam_user_data = SocialAccount.objects.filter(user=request.user)[0]
        user_steam_id = steam_user_data.extra_data.get('steamid')

        # Получение данных FaceIT
        request_for_faceit_data = 'https://api.faceit.com/search/v1/?limit=3&query=' + user_steam_id
        faceit_user_data = requests.get(request_for_faceit_data).json().get('payload', {}).get('players', {}).get('results')
        faceit_user_data = faceit_user_data[0] if faceit_user_data else None

    return {'steam_user_data': steam_user_data, 'faceit_user_data': faceit_user_data}


class MainPage(ListView):
    """Класс представления главной страницы"""

    def get(self, request, *args, **kwargs):
        """Обработка get-запроса"""
        context = {}
        context.update(get_all_user_data(request))
        return render(request, 'main/main.html', context)


class ProfilePage(DetailView):
    """Класс представления страницы профиля пользователя"""

    def get(self, request: WSGIRequest, *args, **kwargs):
        """Обработка get-запроса"""

        # Редирект для администраторов
        if request.user.is_superuser:
            return render(request, 'main/admin_profile.html')

        # Редирект на главную, если пользователь не авторизован
        if not request.user.is_authenticated:
            return redirect('main')

        context = {}
        context.update(get_all_user_data(request))
        return render(request, 'main/profile.html', context)
