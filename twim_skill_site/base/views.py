from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from main.models import Lobby
from main.services import get_user_lobby_data
from users.models import User
from users.services import get_steam_faceit_user_data


class MainPage(ListView):
    """Главная страницы"""

    model = User
    context_object_name = 'lobbies'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Обработка get-запроса"""
        user = request.user
        context = {
            'user_data': get_steam_faceit_user_data(user),
            'user_lobby_data': get_user_lobby_data(user),
            'lobbies': Lobby.objects.all(),
        }

        return render(request, 'base/main.html', context)


class ProfilePage(DetailView):
    """Страница профиля пользователя"""

    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse | HttpResponseRedirect:
        """Обработка get-запроса"""

        user = request.user

        # Редирект для администраторов
        if user.is_superuser:
            return render(request, 'main/admin_profile.html')

        # Редирект на главную, если пользователь не авторизован
        if not user.is_authenticated:
            return redirect('main')

        # Получение данных авторизованного пользователя и открытие страницы профиля
        context = {
            'user_data': get_steam_faceit_user_data(user),
            'user_lobby_data': get_user_lobby_data(user),
        }

        return render(request, 'base/profile.html', context)
