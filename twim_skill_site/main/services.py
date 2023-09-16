from main.models import PlayerLobby


def get_player_lobby(user_id: int) -> PlayerLobby:
    """Получить лобби, в котором находится пользователь"""
    return PlayerLobby.objects.get(id_user=user_id, in_lobby=True)


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
