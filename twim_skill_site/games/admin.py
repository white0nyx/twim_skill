from django.contrib import admin
from .models import *


@admin.register(Map)
class GameMapAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'image')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(GameType)
class GameTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(GameStatus)
class GameStatusAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(GameMode)
class GameModeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Veto)
class VetoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(VetoGameModeInfo)
class VetoGameModeInfoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game_mode', 'veto')
    list_filter = ('game_mode', 'veto')
    search_fields = ('game_mode',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'map', 'status', 'date_start', 'date_end')
    list_filter = ('map', 'status')
    search_fields = ('lobby',)


@admin.register(PlayerMatchInfo)
class PlayerGameInfoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game', 'user')
    list_filter = ('game', 'user',)
    search_fields = ('game', 'user')


@admin.register(PlayerStatisticInGame)
class PlayerStatisticInGameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game', 'user', 'kills', 'assists', 'deaths', 'headshots_count', 'kr_ratio', 'mvp')
    list_filter = ('game', 'user',)
    search_fields = ('game', 'user')
