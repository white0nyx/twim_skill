from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import user_logged_in
from django.core.handlers.wsgi import WSGIRequest
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.views import View
from django.utils import timezone
from django.views.generic import ListView, DetailView
from main.models import *

import requests
import logging

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

class MainPage(ListView):
    """Класс представления главной страницы"""

    def get(self, request, *args, **kwargs):
        """Обработка get-запроса"""
        context = {}
        user_in_lobby = False
        context.update(get_all_user_data(request))

        if request.user.is_authenticated and not request.user.is_superuser:
            user_in_lobby = PlayersLobby.objects.filter(id_user=request.user.id, in_lobby=True).exists()

            if user_in_lobby:
                user_lobby = PlayersLobby.objects.get(id_user=request.user.id, in_lobby=True)
                lobby_slug = user_lobby.id_lobby.slug
                context['user_lobby_slug'] = lobby_slug

        context['user_in_lobby'] = user_in_lobby
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


# @receiver(user_logged_in)
# def create_user_profile(sender, request, user, **kwargs):
#     if user.socialaccount_set.filter(provider='steam').exists():
#         steam_user_data = user.socialaccount_set.get(provider='steam')
#         steam_user_extra_data = steam_user_data.extra_data
#
#         if not User.objects.filter(nickname=user.username).exists():
#             User.objects.create(
#                 nickname=steam_user_extra_data.get('personaname'),
#                 id_role=1,
#                 registration_date=timezone.now().date(),
#                 last_enter_date=timezone.now(),
#                 steam_url=steam_user_extra_data.get('profileurl'),
#                 faciet_url=steam_user_extra_data.get('profileurl'),
#             )



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

            player_lobby = PlayersLobby.objects.create(
                id_lobby=lobby,
                id_user=request.user.id,
                team_id=1,
                in_lobby=True
            )

            return redirect('detail_lobby', slug=slug)

class DetailLobby(View):
    def get(self, request, slug):
        lobby = Lobby.objects.get(slug=slug)
        players_in_lobby = PlayersLobby.objects.filter(id_lobby=lobby, in_lobby=True).count()

        return render(request, 'main/detail_lobby.html', {'lobby': lobby, 'players_in_lobby': players_in_lobby})


def leave_f_lobby(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        # Определяем в каком лобби пользователь
        player_lobby = PlayersLobby.objects.get(id_user=user_id, in_lobby=True)
        # Проверка на то, сколько игроков в лобби
        players_in_lobby = PlayersLobby.objects.filter(id_lobby=player_lobby.id_lobby, in_lobby=True).count()

        if players_in_lobby <= 1:
            lobby_to_delete = player_lobby.id_lobby
            player_lobby.delete()

            lobby_to_delete.delete()

        else:
            player_lobby.in_lobby = False
            player_lobby.save()

        return redirect('main')