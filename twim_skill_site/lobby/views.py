import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from django.views.decorators.csrf import csrf_exempt

from lobby.forms import LobbyPasswordForm
from lobby.models import *
from lobby.services import *
from users.services import get_steam_faceit_user_data

MINIMAL_BET = 0
MIN_LEVEL_ENTRE = 0
MAX_LEVEL_ENTRE = 10


class CreateLobbyPage(View):
    """Страница создания лобби"""

    @staticmethod
    def get(request) -> HttpResponse:
        """Обработчик get-запроса"""

        if not request.user.is_authenticated:
            messages.error(request, 'Для создания лобби необходимо авторизоваться.')
            return redirect('main')

        user = request.user
        player_in_lobby = get_player_lobby(user)

        context = {
            'games_types': GameType.objects.all(),
            'games_modes': GameMode.objects.all(),
            'vetos': Veto.objects.all(),
            'pools': Pool.objects.all(),
            'maps': Map.objects.all(),
        }

        if player_in_lobby:
            messages.error(request, 'Вы уже находитесь в другом лобби.')
            return redirect('detail_lobby', slug=player_in_lobby.lobby.slug)

        return render(request, 'lobby/create_lobby.html', context)

    @staticmethod
    def post(request) -> HttpResponseRedirect:
        """Обработчик post-запроса создания лобби"""

        print(request.POST)

        user = request.user
        context = {
            'games_types': GameType.objects.all(),
            'games_modes': GameMode.objects.all(),
            'vetos': Veto.objects.all(),
            'pools': Pool.objects.all(),
            'maps': Map.objects.all(),
        }

        game_map = request.POST.get('maps')
        bet = Decimal(request.POST.get('bet')) if request.POST.get('bet') else MINIMAL_BET
        max_lvl_enter = int(request.POST.get('max_lvl_enter') if request.POST.get('max_lvl_enter') else MAX_LEVEL_ENTRE)
        min_lvl_enter = int(request.POST.get('min_lvl_enter') if request.POST.get('min_lvl_enter') else MIN_LEVEL_ENTRE)
        slug = slugify(f"{game_map}-{user.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}")

        # Валидация пользователя для создания лобби
        check_user_for_create_lobby(request, user, min_lvl_enter, max_lvl_enter, bet)
        if messages.get_messages(request):
            return render(request, 'lobby/create_lobby.html', context)

        # Создание лобби и игр
        create_match_lobby_and_games(request, min_lvl_enter, max_lvl_enter, bet, slug)

        return redirect('detail_lobby', slug=slug)


class DetailLobbyPage(View):
    """Страница с деталями лобби"""

    @staticmethod
    def get(request: WSGIRequest, slug: str) -> HttpResponse:
        user = request.user
        lobby = Lobby.objects.get(slug=slug)
        count_players_in_lobby = PlayerLobby.objects.filter(lobby=lobby, in_lobby=True).count()

        context = {
            'title': f'Лобби №{lobby.pk}',
            'lobby': lobby,
            'count_players_in_lobby': count_players_in_lobby,
            'user_data': get_steam_faceit_user_data(user),
            'user_lobby_data': get_user_lobby_data(user),
            'player_in_lobby': get_player_lobby(user),
            'games': Game.objects.filter(match=lobby.match).order_by('pk'),
            'players': PlayerLobby.objects.filter(lobby=lobby)
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

        # Валидация пользователя для присоединения к лобби
        check_user_for_join_lobby(request, request.user, slug)
        if not messages.get_messages(request):
            create_player_lobby(request.user, slug)

        return redirect('detail_lobby', slug=slug)

    @staticmethod
    def post(request: WSGIRequest, slug: str) -> HttpResponse | HttpResponseRedirect:

        # Валидация пользователя для присоединения к лобби
        check_user_for_join_lobby(request, request.user, slug)
        if messages.get_messages(request):
            return redirect('detail_lobby', slug=slug)

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


@csrf_exempt
def game_action(request):
    """Изменение статуса игры"""
    if request.method == 'POST':
        game_id = request.POST.get('game_id', None)
        new_game_status = request.POST.get('game_status', None)
        game = Game.objects.get(pk=game_id)

        if new_game_status == 'running':
            game.date_start = datetime.datetime.now()

        elif new_game_status == 'finished':
            game.date_end = datetime.datetime.now()

        game.status = GameStatus.objects.get(name=new_game_status)
        game.save()
        return redirect(request.META['HTTP_REFERER'])
