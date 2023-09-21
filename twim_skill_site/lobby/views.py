from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from lobby.models import *
from lobby.services import *
from users.services import get_steam_faceit_user_data


class CreateLobbyPage(View):
    """Страница создания лобби"""

    @staticmethod
    def get(request) -> HttpResponse:
        """Обработчик get-запроса"""
        return render(request, 'lobby/create_lobby.html')

    @staticmethod
    def post(request) -> HttpResponseRedirect:
        """Обработчик post-запроса создания лобби"""
        if request.user.is_authenticated:
            user_id = request.user.id
            game_map = request.POST.get('map', 'Dust2')
            bet = request.POST.get('bet', 500)
            password_lobby = request.POST.get('password_lobby', '')
            max_lvl_enter = request.POST.get('max_lvl_enter', 3)
            slug = slugify(f"{game_map}-{user_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}")

            lobby = Lobby.objects.create(
                id_leader=user_id,
                map=game_map,
                bet=bet,
                password_lobby=password_lobby,
                max_lvl_enter=max_lvl_enter,
                deleted=False,
                slug=slug
            )

            PlayerLobby.objects.create(
                id_lobby=lobby,
                id_user=request.user.id,
                team_id=1,
                in_lobby=True
            )

            return redirect('detail_lobby', slug=slug)


class DetailLobbyPage(View):
    """Страница с деталями лобби"""

    @staticmethod
    def get(request: WSGIRequest, slug: str) -> HttpResponse:
        lobby = Lobby.objects.get(slug=slug)
        count_players_in_lobby = PlayerLobby.objects.filter(id_lobby=lobby, in_lobby=True).count()

        user = request.user
        context = {
            'lobby': lobby,
            'count_players_in_lobby': count_players_in_lobby,
            'user_data': get_steam_faceit_user_data(user),
            'user_lobby_data': get_user_lobby_data(user)
        }

        return render(request, 'lobby/detail_lobby.html', context)


def leave_f_lobby(request: WSGIRequest) -> HttpResponse:
    """Покинуть лобби"""

    user = request.user
    if user.is_authenticated:

        # Определяем в каком лобби пользователь
        lobby = get_player_lobby(user)

        if get_count_players_in_lobby(lobby) <= 1:
            leave_lobby_with_delete(lobby)
        else:
            leave_lobby(lobby)

        return redirect('main')


class JoinLobby(View):
    """Присоединение к лобби"""

    @staticmethod
    def get(request: WSGIRequest, slug: str) -> HttpResponse | HttpResponseRedirect:
        """Обработка get-запроса"""

        user = request.user

        # Редирект неавторизованного пользователя на главную страницу
        if not user.is_authenticated:
            messages.error(request, 'Пройдите авторизацию для присоединения к лобби.')
            return redirect('main')

        # Редирект пользователя, который уже находится в лобби
        elif get_player_lobby(user):
            messages.error(request, 'Вы уже находитесь в данном лобби.')
            return redirect('main')

        # Ошибка slug'а лобби
        elif not get_lobby_by_slug(slug):
            messages.error(request, 'Лобби с указанным slug не найдено.')
            return redirect('main')

        # Сохранение пользователя в лобби
        PlayerLobby.objects.create(
            id_lobby=Lobby.objects.get(slug=slug),
            id_user=request.user.id,
            team_id=1,
            in_lobby=True,
        )

        return redirect('detail_lobby', slug=slug)
