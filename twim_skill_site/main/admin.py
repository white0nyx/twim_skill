from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'id_role', 'registration_date', 'last_enter_date', 'steam_url', 'faciet_url')


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_leader', 'map', 'bet', 'password_lobby', 'max_lvl_enter', 'deleted')
    list_filter = ('deleted',)
    search_fields = ('id_leader', 'map')