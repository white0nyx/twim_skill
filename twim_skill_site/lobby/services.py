import logging

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from users.services import get_steam_faceit_user_data

from lobby.models import PlayerLobby, Lobby

logger = logging.getLogger(__name__)


def get_user_lobby_data(user: AbstractUser) -> dict:
    """Получить данные пользователя"""

    user_data = {'user_in_lobby': False}
    if user.is_authenticated and not user.is_superuser:

        user_lobby = get_player_lobby(user)
        user_data['user_in_lobby'] = user_lobby

        if user_lobby:
            user_data['user_lobby_slug'] = user_lobby.lobby.slug

    return user_data


def get_lobby_by_slug(slug: str) -> Lobby | None:
    """Получить лобби по slug'у"""
    lobby = Lobby.objects.filter(slug=slug)
    return lobby[0] if lobby else None


def get_player_lobby(user: AbstractUser) -> PlayerLobby | None:
    """Получить лобби, в котором находится пользователь"""
    player_lobby = PlayerLobby.objects.filter(user=user, in_lobby=True)
    return player_lobby[0] if player_lobby else None


def get_count_players_in_lobby(lobby: PlayerLobby) -> int:
    """Получить количество игроков в лобби"""
    return PlayerLobby.objects.filter(lobby=lobby.lobby, in_lobby=True).count()


def leave_lobby(lobby: PlayerLobby) -> None:
    """Покинуть лобби (без удаления)"""
    lobby.in_lobby = False
    lobby.save()


def leave_lobby_with_delete(lobby: PlayerLobby) -> None:
    """Покинуть лобби с его удалением"""
    lobby_to_delete = lobby.lobby
    lobby.delete()
    lobby_to_delete.delete()

def check_user(request: WSGIRequest, user: AbstractUser, slug: str) -> tuple[HttpResponse | HttpResponseRedirect, Lobby | None]:
    """Проверка пользователя перед входом в лобби"""
    lobby = get_lobby_by_slug(slug)
    user_lobby = get_player_lobby(user)
    user_data = get_steam_faceit_user_data(user)
    user_level = user_data['faceit_user_data']['games'][0]['skill_level'] if user_data['faceit_user_data'] else None

    if not user.is_authenticated:
        messages.error(request, 'Пройдите авторизацию для присоединения к лобби.')
        return HttpResponseRedirect('main'), None

    if user_lobby:
        messages.error(request, 'Вы уже находитесь в данном лобби.')
        return HttpResponseRedirect('main'), None

    if not lobby:
        messages.error(request, 'Лобби с указанным slug не найдено.')
        return HttpResponseRedirect('main'), None

    if not user_level or user_level < lobby.min_lvl_enter and user_level > lobby.max_lvl_enter:
        messages.error(request, 'Ваш уровень Faceit не соответствует требованиям лобби.')
        return HttpResponseRedirect(reverse('detail_lobby', args=[slug])), None

    return user, lobby


def create_player_lobby(user: AbstractUser, slug: str):
    """Присоединение пользователя к лобби"""
    PlayerLobby.objects.create(
        lobby=Lobby.objects.get(slug=slug),
        user=user,
        team_id=1,
        in_lobby=True,
    )

def check_user(request: WSGIRequest, user: AbstractUser, slug: str) -> tuple[HttpResponse | HttpResponseRedirect, Lobby | None]:
    """Проверка пользователя перед входом в лобби"""
    lobby = get_lobby_by_slug(slug)
    user_lobby = get_player_lobby(user)
    user_data = get_steam_faceit_user_data(user)
    user_level = user_data['faceit_user_data']['games'][0]['skill_level']

    if not user_level or (user_level < lobby.min_lvl_enter or user_level > lobby.max_lvl_enter):
        messages.error(request, 'Ваш уровень faciet не соотвествует условиям лобби.')
        return HttpResponseRedirect(reverse('detail_lobby', args=[slug])), None

    if not user.is_authenticated:
        messages.error(request, 'Пройдите авторизацию для присоединения к лобби.')
        return HttpResponseRedirect('main'), None

    if user_lobby:
        messages.error(request, 'Вы уже находитесь в данном лобби.')
        return HttpResponseRedirect(reverse('detail_lobby', args=[slug])), None

    if not lobby:
        messages.error(request, 'Лобби с указанным slug не найдено.')
        return HttpResponseRedirect('main'), None

    return user, lobby


def create_player_lobby(user: AbstractUser, slug: str):
    """Присоединение пользователя к лобби"""
    PlayerLobby.objects.create(
        lobby=Lobby.objects.get(slug=slug),
        user=user,
        team_id=1,
        in_lobby=True,
    )
