from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from main.models import *

from main.services import get_player_lobby, get_count_players_in_lobby, leave_lobby_with_delete, leave_lobby, \
    get_user_lobby_data, get_steam_faceit_user_data, get_lobby_by_slug


class MainPage(ListView):
    """Главная страницы"""

    def get(self, request, *args, **kwargs):
        """Обработка get-запроса"""
        user = request.user
        context = {
            'user_data': get_steam_faceit_user_data(user),
            'user_lobby_data': get_user_lobby_data(user),
        }
        return render(request, 'main/main.html', context)


class ProfilePage(DetailView):
    """Страница профиля пользователя"""

    def get(self, request: WSGIRequest, *args, **kwargs):
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
        return render(request, 'main/profile.html', context)


class CreateLobby(View):
    """Страница создания лобби"""

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


class DetailLobbyPage(View):
    """Страница с деталями лобби"""
    def get(self, request, slug):
        lobby = Lobby.objects.get(slug=slug)
        players_in_lobby = PlayerLobby.objects.filter(id_lobby=lobby, in_lobby=True).count()

        user = request.user
        context = {
            'lobby': lobby,
            'players_in_lobby': players_in_lobby,
            'user_data': get_steam_faceit_user_data(user),
            'user_lobby_data': get_user_lobby_data(user)
        }

        return render(request, 'main/detail_lobby.html', context)


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
