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


# <-------------- Вето -------------->
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


# <-------------- Игра -------------->
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'map', 'status', 'date_start', 'date_end')
    list_filter = ('map', 'status')
    search_fields = ('lobby',)


@admin.register(PlayerGameInfo)
class PlayerGameInfoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game', 'user')
    list_filter = ('game', 'user',)
    search_fields = ('game', 'user')


@admin.register(PlayerStatisticInGame)
class PlayerStatisticInGameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game', 'user', 'kills', 'assists', 'deaths', 'headshots_count', 'kr_ratio', 'mvp')
    list_filter = ('game', 'user',)
    search_fields = ('game', 'user')


# <-------------- Пулы -------------->
@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'pool_group')
    list_filter = ('name', 'pool_group',)
    search_fields = ('name', 'pool_group')


@admin.register(PoolMapInfo)
class PoolMapInfoAdmin(admin.ModelAdmin):
    list_display = ('pool', 'map')
    list_filter = ('pool', 'map',)
    search_fields = ('pool', 'map')


@admin.register(PoolGroup)
class PoolGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('pool',)
