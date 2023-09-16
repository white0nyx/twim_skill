from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from main.models import *

import requests
import logging

from main.services import get_player_lobby, get_count_players_in_lobby, leave_lobby_with_delete, \
    leave_lobby

logger = logging.getLogger(__name__)


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
        faceit_data = requests.get(request_for_faceit_data).json()
        faceit_user_data = faceit_data.get('payload', {}).get('players', {}).get('results')
        logger.info(f'user_steam_id={user_steam_id} | faceit_user_data = {faceit_user_data}')
        faceit_user_data = faceit_user_data[0] if faceit_user_data else None

    return {'steam_user_data': steam_user_data, 'faceit_user_data': faceit_user_data}


class UserInLobby(View):
    @staticmethod
    def get_user_data(request):
        user_data = {}
        user_data['user_in_lobby'] = False

        if request.user.is_authenticated and not request.user.is_superuser:
            user_data['user_in_lobby'] = PlayerLobby.objects.filter(id_user=request.user.id, in_lobby=True).exists()

            if user_data['user_in_lobby']:
                user_lobby = PlayerLobby.objects.get(id_user=request.user.id, in_lobby=True)
                user_data['user_lobby_slug'] = user_lobby.id_lobby.slug

        user_data.update(get_all_user_data(request))
        return user_data


class MainPage(ListView):
    """Класс представления главной страницы"""

    def get(self, request, *args, **kwargs):
        """Обработка get-запроса"""

        context = UserInLobby.get_user_data(request)
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

        context = UserInLobby.get_user_data(request)
        return render(request, 'main/profile.html', context)


class CreateLobby(View):
    def get(self, request):
        return render(request, 'main/create_lobby.html')

    def post(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            map = request.POST.get('map', 'Dust2')
            bet = request.POST.get('bet', 500)
            password_lobby = request.POST.get('password_lobby', '')
            max_lvl_enter = request.POST.get('max_lvl_enter', 3)
            slug = slugify(f"{map}-{user_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}")

            lobby = Lobby.objects.create(
                id_leader=user_id,
                map=map,
                bet=bet,
                password_lobby=password_lobby,
                max_lvl_enter=max_lvl_enter,
                deleted=False,
                slug=slug
            )

            player_lobby = PlayerLobby.objects.create(
                id_lobby=lobby,
                id_user=request.user.id,
                team_id=1,
                in_lobby=True
            )

            return redirect('detail_lobby', slug=slug)


class DetailLobby(View):
    def get(self, request, slug):
        lobby = Lobby.objects.get(slug=slug)
        players_in_lobby = PlayerLobby.objects.filter(id_lobby=lobby, in_lobby=True).count()
        context = UserInLobby.get_user_data(request)
        print(context)

        return render(request, 'main/detail_lobby.html',
                      {'lobby': lobby, 'players_in_lobby': players_in_lobby, 'context': context})


def leave_f_lobby(request):
    """Покинуть лобби"""
    if request.user.is_authenticated:

        # Определяем в каком лобби пользователь
        lobby = get_player_lobby(request.user.id)

        if get_count_players_in_lobby(lobby) <= 1:
            leave_lobby_with_delete(lobby)
        else:
            leave_lobby(lobby)

        return redirect('main')


class JoinLobby(View):
    def get(self, request, slug):
        if request.user.is_authenticated:
            user_in_lobby = PlayerLobby.objects.filter(id_user=request.user.id, in_lobby=True).exists()

            if not user_in_lobby:
                try:
                    lobby = Lobby.objects.get(slug=slug)
                    player_lobby = PlayerLobby.objects.create(
                        id_lobby=lobby,
                        id_user=request.user.id,
                        team_id=1,
                        in_lobby=True
                    )

                    return redirect('detail_lobby', slug=slug)
                except Lobby.DoesNotExist:
                    messages.error(request, 'Лобби с указанным slug не найдено.')
                    pass

                return redirect('detail_lobby', slug=slug)  # Возвращаем пользователя на страницу лобби
            else:
                return redirect('main')
