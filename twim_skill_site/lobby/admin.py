from django.contrib import admin
from .models import *


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'leader', 'map', 'bet', 'password_lobby', 'max_lvl_enter', 'slug')
    search_fields = ('leader', 'map')


@admin.register(PlayerLobby)
class PlayersLobbyAdmin(admin.ModelAdmin):
    list_display = ('lobby', 'user', 'team_id', 'in_lobby', 'time_enter')
    list_filter = ('team_id', 'in_lobby', 'time_enter')
    search_fields = ('lobby__slug', 'user__nickname')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('type', 'mode', 'veto')
    list_filter = ('type', 'mode')


class PlayersLobby(admin.ModelAdmin):
    list_display = ('lobby', 'user', 'team_id', 'in_lobby')
