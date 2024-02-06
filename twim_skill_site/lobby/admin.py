from django.contrib import admin

from games.models import PlayerMatch
from .models import *


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'leader')
    search_fields = ('leader',)


@admin.register(PlayerLobby)
class PlayersLobbyAdmin(admin.ModelAdmin):
    list_display = ('lobby', 'user', 'time_enter')
    list_filter = ('time_enter',)
    search_fields = ('user__nickname',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('type', 'mode', 'veto')
    list_filter = ('type', 'mode')


class PlayersLobby(admin.ModelAdmin):
    list_display = ('lobby', 'user', 'team_id', 'in_lobby')

@admin.register(PlayerMatch)
class PlayerMatchAdmin(admin.ModelAdmin):
    list_display = ('match', 'user', 'team')