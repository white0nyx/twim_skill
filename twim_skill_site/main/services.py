from main.models import PlayersLobby


def get_player_lobby(user_id: int) -> PlayersLobby:
    """Получить лобби, в котором находится пользователь"""
    return PlayersLobby.objects.get(id_user=user_id, in_lobby=True)


def get_count_players_in_lobby(lobby: PlayersLobby) -> int:
    """Получить количество игроков в лобби"""
    return PlayersLobby.objects.filter(id_lobby=lobby.id_lobby, in_lobby=True).count()


def leave_lobby(lobby: PlayersLobby) -> None:
    """Покинуть лобби (без удаления)"""
    lobby.in_lobby = False
    lobby.save()


def leave_lobby_with_delete(lobby: PlayersLobby) -> None:
    """Покинуть лобби с его удалением"""
    lobby_to_delete = lobby.id_lobby
    lobby.delete()
    lobby_to_delete.delete()
