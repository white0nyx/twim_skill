from django.contrib import admin
from .models import *


@admin.register(GameMap)
class GameMapAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
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
    list_display = ('pk', 'game', 'user', 'accuracy', 'headshots_count', 'kills', 'deaths')
    list_filter = ('game', 'user',)
    search_fields = ('game', 'user')
