import logging

from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.utils import timezone

from games.models import Map, GameType, GameMode, Veto, Pool, Game, Match, GameStatus, PlayerMatch
from users.models import User
from users.services import get_steam_faceit_user_data

from lobby.models import PlayerLobby, Lobby

logger = logging.getLogger(__name__)


def get_user_lobby_data(user: AbstractUser) -> dict:
    """Получить данные пользователя"""

    user_data = {'user_in_lobby': False}
    if user.is_authenticated and not user.is_superuser:

        user_lobby = is_player_in_lobby(user)
        user_data['user_in_lobby'] = user_lobby

        if user_lobby:
            user_data['user_lobby_slug'] = user_lobby.lobby.slug

    return user_data


def get_lobby_by_slug(slug: str) -> Lobby | None:
    """Получить лобби по slug'у"""
    lobby = Lobby.objects.filter(slug=slug)
    return lobby[0] if lobby else None

def get_user_match(user: User):
    match = PlayerMatch.objects.filter(user=user)
    return match[0] if match else None


def is_player_in_lobby(user: AbstractUser) -> PlayerLobby | None:
    """Проверить находится ли пользователь в лобби"""
    player_lobby = PlayerLobby.objects.filter(user=user)
    return player_lobby[0] if player_lobby else False


def get_count_players_in_lobby(lobby: PlayerLobby) -> int:
    """Получить количество игроков в лобби"""
    return PlayerLobby.objects.filter(lobby=lobby.lobby, in_lobby=True).count()


def leave_lobby(lobby: PlayerLobby) -> None:
    """Покинуть лобби (без удаления)"""
    lobby.in_lobby = False
    lobby.save()


def delete_match_and_games(match: Match) -> None:
    """Удалить матч и игры, принадлежащие ему"""
    for game in Game.objects.filter(match=match):
        game.delete()

    match.delete()


def leave_lobby_with_delete(player_lobby: PlayerLobby) -> None:
    """Покинуть лобби с его удалением"""
    lobby_to_delete = player_lobby.lobby
    player_lobby.delete()
    lobby_to_delete.delete()
    delete_match_and_games(lobby_to_delete.match)

def get_players_lobby_sorted_by_time(lobby: Lobby) -> list:
    """Получить список всех участников лобби, отсортированных по времени входа"""
    players = (
        PlayerLobby.objects
        .filter(lobby=lobby, in_lobby=True)
        .order_by('time_enter')
        .select_related('user')
    )
    return list(players)


def check_user_for_join_lobby(request: WSGIRequest, user: User, slug: str) -> None:
    """Проверка пользователя перед входом в лобби"""
    lobby = get_lobby_by_slug(slug)
    user_lobby = is_player_in_lobby(user)
    user_data = get_steam_faceit_user_data(user)
    user_level = user_data['faceit_user_data']['games'][0]['skill_level']

    if not user_level or (user_level < lobby.min_lvl_enter or user_level > lobby.max_lvl_enter):
        messages.error(request, 'Ваш уровень faceit не соответствует условиям лобби.')

    if not user.is_authenticated:
        messages.error(request, 'Пройдите авторизацию для присоединения к лобби.')

    if user_lobby:
        messages.error(request, 'Вы уже находитесь в данном лобби.')

    if not lobby:
        messages.error(request, 'Лобби с указанным slug не найдено.')

    if lobby.bet > user.balance:
        messages.error(request, 'Недостаточно TWIM-COIN на балансе для подключения к лобби.')


def check_user_for_create_lobby(request: WSGIRequest, min_lvl_enter: int, max_lvl_enter: int,
                                bet: Decimal) -> None:
    user = request.user
    user_level = get_steam_faceit_user_data(user)['faceit_user_data']['games'][0]['skill_level']

    if user_level < int(min_lvl_enter):
        messages.error(request, 'Минимальный уровень лобби выше вашего уровня.')

    if user_level > int(max_lvl_enter):
        messages.error(request, 'Максимальный уровень лобби ниже вашего уровня.')

    if user.balance < bet:
        messages.error(request, 'Недостаточно TWIM-COIN на балансе для создания лобби.')

    if is_player_in_lobby(user):
        messages.error(request, 'Вы уже находитесь в другом лобби.')


def create_player_lobby(user: AbstractUser, slug: str):
    """Присоединение пользователя к лобби"""
    PlayerLobby.objects.create(
        lobby=Lobby.objects.get(slug=slug),
        user=user,
        team_id=0,
        in_lobby=True,
    )


def create_match_lobby_and_games(
        request: WSGIRequest,
        min_lvl_enter: int,
        max_lvl_enter: int,
        bet: Decimal,
        game_map: str,) -> Match:
    """Создание матча, лобби и игр"""

    user = request.user
    game_type = GameType.objects.get(name=request.POST.get('game_type'))
    game_mode = GameMode.objects.get(name=request.POST.get('game_mode'))
    veto = Veto.objects.get(name=request.POST.get('veto'))
    pool = request.POST.get('pool')
    password_lobby = request.POST.get('password_lobby')
    game_map = Map.objects.get(name=game_map)

    match = Match.objects.create(
        type=game_type,
        mode=game_mode,
        veto=veto,
        map=game_map,
        pool=Pool.objects.get(name=pool),
        bet=bet,
        max_lvl_enter=max_lvl_enter,
        min_lvl_enter=min_lvl_enter,
    )

    lobby = Lobby.objects.create(
        leader=user,
        match=match,
        password_lobby=password_lobby,
    )

    PlayerLobby.objects.create(
        lobby=lobby,
        user=user,
        time_enter=timezone.now()
    )

    PlayerMatch.objects.create(
        match=match,
        user=user,
        team=1,
    )

    for i in range(int(game_mode.name[-1])):
        Game.objects.create(
            date_start=None, date_end=None,
            map=game_map,
            status=GameStatus.objects.get(name='preparing'),
            match=match
        )

    return match