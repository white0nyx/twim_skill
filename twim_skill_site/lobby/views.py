from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from lobby.forms import LobbyPasswordForm
from games.models import Map, GameType, GameMode, Veto, Pool
from lobby.models import *
from lobby.services import *
from users.services import get_steam_faceit_user_data


class CreateLobbyPage(View):
    """Страница создания лобби"""

    @staticmethod
    def get(request) -> HttpResponse:
        """Обработчик get-запроса"""

        context = {
            'games_types': GameType.objects.all(),
            'games_modes': GameMode.objects.all(),
            'vetos': Veto.objects.all(),
            'pools': Pool.objects.all(),
            'maps': Map.objects.all(),
        }
        return render(request, 'lobby/create_lobby.html', context)

    @staticmethod
    def post(request) -> HttpResponseRedirect:
        """Обработчик post-запроса создания лобби"""

        user = request.user
        insufficient_balance = False

        if user.is_authenticated:
            print(request.POST)
            game_type = request.POST.get('game_type')
            game_mode = request.POST.get('game_mode')
            veto = request.POST.get('veto')
            pool = request.POST.get('pool')
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
                    game_type=GameType.objects.get(name=game_type),
                    game_mode=GameMode.objects.get(name=game_mode),
                    veto=Veto.objects.get(name=veto),
                    pool=Pool.objects.get(name=pool),
                    bet=bet,
                    password_lobby=password_lobby,
                    max_lvl_enter=max_lvl_enter,
                    min_lvl_enter=min_lvl_enter,
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
            'games_types': GameType.objects.all(),
            'games_modes': GameMode.objects.all(),
            'vetos': Veto.objects.all(),
            'pools': Pool.objects.all(),
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

    def get(self, request: WSGIRequest, slug: str) -> HttpResponse | HttpResponseRedirect:
        error = check_user(request, request.user, slug)

        if error:
            return error

        create_player_lobby(request.user, slug)
        return redirect('detail_lobby', slug=slug)

    def post(self, request: WSGIRequest, slug: str) -> HttpResponse | HttpResponseRedirect:
        error = check_user(request, request.user, slug)

        if error:
            return error

        lobby = get_lobby_by_slug(slug)

        form = LobbyPasswordForm(request.POST)
        if lobby.password_lobby and form.is_valid():
            entered_password = form.cleaned_data['password']
            if entered_password == lobby.password_lobby:
                create_player_lobby(request.user, slug)
                return redirect('detail_lobby', slug=slug)
            else:
                messages.error(request, 'Неверный пароль для присоединения к лобби.')
                return redirect('detail_lobby', slug=slug)

        return redirect('detail_lobby', slug=slug)
