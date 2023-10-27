from decimal import Decimal

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from games.models import Map
from lobby.models import *
from lobby.services import *
from users.services import get_steam_faceit_user_data


class CreateLobbyPage(View):
    """Страница создания лобби"""

    @staticmethod
    def get(request) -> HttpResponse:
        """Обработчик get-запроса"""

        context = {
            'maps': Map.objects.all(),
        }
        return render(request, 'lobby/create_lobby.html', context)

    @staticmethod
    def post(request) -> HttpResponseRedirect:
        """Обработчик post-запроса создания лобби"""

        user = request.user
        insufficient_balance = False

        if user.is_authenticated:
            game_map = request.POST.get('maps')
            bet = Decimal(request.POST.get('bet')) if request.POST.get('bet') else 0
            password_lobby = request.POST.get('password_lobby')
            max_lvl_enter = request.POST.get('max_lvl_enter') if request.POST.get('max_lvl_enter') else 10
            min_lvl_enter = request.POST.get('min_lvl_enter') if request.POST.get('min_lvl_enter') else 0
            slug = slugify(f"{game_map}-{user.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}")

            if user.balance >= bet:
                lobby = Lobby.objects.create(
                    leader=user,
                    map=game_map,
                    bet=bet,
                    password_lobby=password_lobby,
                    max_lvl_enter=max_lvl_enter,
                    min_lvl_enter=min_lvl_enter,
                    deleted=False,
                    slug=slug
                )

                PlayerLobby.objects.create(
                    lobby=lobby,
                    user=user,
                    team_id=1,
                    in_lobby=True
                )

                return redirect('detail_lobby', slug=slug)
            else:
                insufficient_balance = True

        context = {
            'insufficient_balance': insufficient_balance,
            'maps': Map.objects.all(),
        }

        return render(request, 'lobby/create_lobby.html', context)


class DetailLobbyPage(View):
    """Страница с деталями лобби"""

    @staticmethod
    def get(request: WSGIRequest, slug: str) -> HttpResponse:
        lobby = Lobby.objects.get(slug=slug)
        count_players_in_lobby = PlayerLobby.objects.filter(lobby=lobby, in_lobby=True).count()

        user = request.user
        context = {
            'title': f'Лобби №{lobby.pk}',
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
            lobby=Lobby.objects.get(slug=slug),
            user=user,
            team_id=1,
            in_lobby=True,
        )

        return redirect('detail_lobby', slug=slug)
