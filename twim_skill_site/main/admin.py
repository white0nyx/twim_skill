from django.contrib import admin
from .models import *


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_leader', 'map', 'bet', 'password_lobby', 'max_lvl_enter', 'deleted', 'slug')
    list_filter = ('deleted',)
    search_fields = ('id_leader', 'map')


@admin.register(PlayerLobby)
class PlayersLobbyAdmin(admin.ModelAdmin):
    list_display = ('id_lobby', 'id_user', 'team_id', 'in_lobby')
    list_filter = ('team_id', 'in_lobby')
    search_fields = ('id_lobby__slug', 'id_user__nickname')


class PlayersLobby(admin.ModelAdmin):
    list_display = ('id_lobby', 'id_user', 'team_id', 'in_lobby')
