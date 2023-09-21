import logging

from django.contrib.auth.models import AbstractUser

from main.models import PlayerLobby, Lobby

logger = logging.getLogger(__name__)


def get_user_lobby_data(user: AbstractUser) -> dict:
    """Получить данные пользователя"""

    user_data = {'user_in_lobby': False}
    if user.is_authenticated and not user.is_superuser:

        user_lobby = get_player_lobby(user)
        user_data['user_in_lobby'] = user_lobby

        if user_lobby:
            user_data['user_lobby_slug'] = user_lobby.id_lobby.slug

    return user_data


def get_lobby_by_slug(slug: str) -> Lobby | None:
    """Получить лобби по slug'у"""
    lobby = Lobby.objects.filter(slug=slug)
    return lobby[0] if lobby else None


def get_player_lobby(user: AbstractUser) -> PlayerLobby | None:
    """Получить лобби, в котором находится пользователь"""
    player_lobby = PlayerLobby.objects.filter(id_user=user.pk, in_lobby=True)
    return player_lobby[0] if player_lobby else None


def get_count_players_in_lobby(lobby: PlayerLobby) -> int:
    """Получить количество игроков в лобби"""
    return PlayerLobby.objects.filter(id_lobby=lobby.id_lobby, in_lobby=True).count()


def leave_lobby(lobby: PlayerLobby) -> None:
    """Покинуть лобби (без удаления)"""
    lobby.in_lobby = False
    lobby.save()


def leave_lobby_with_delete(lobby: PlayerLobby) -> None:
    """Покинуть лобби с его удалением"""
    lobby_to_delete = lobby.id_lobby
    lobby.delete()
    lobby_to_delete.delete()
