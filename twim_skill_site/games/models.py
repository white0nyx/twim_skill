from django.db import models

from lobby.models import Lobby
from users.models import User


class GameMap(models.Model):
    """Модель карты игры"""
    name = models.CharField(max_length=255, verbose_name='Название')
    # link = models.URLField()

    def __str__(self):
        return f'Карта: {self.name}_{self.pk}'


class GameType(models.Model):
    """Модель типа игры"""
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return f'Тип игры: {self.name}_{self.pk}'


class GameStatus(models.Model):
    """Модель статуса игры"""
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return f'Статус игры: {self.name}_{self.pk}'


class Game(models.Model):
    """Модель матча (игры)"""
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='+', verbose_name='Лобби')
    map = models.ForeignKey(GameMap, on_delete=models.CASCADE, related_name='+', verbose_name='Карта')
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE, related_name='+', verbose_name='Тип')
    status = models.ForeignKey(GameStatus, on_delete=models.CASCADE, related_name='+', verbose_name='Статус')
    date_start = models.DateTimeField(verbose_name='Дата начала')
    date_end = models.DateTimeField(verbose_name='Дата окончания')

    def __str__(self):
        return f'Игра_{self.pk}'


class PlayerGameInfo(models.Model):
    """Модель записи игрока матча"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='+', verbose_name='Матч')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', verbose_name='Игрок')

    def __str__(self):
        return f'Информация_{self.pk} о user_{self.user.primary_key} в игре {self.game.primary_key}'


class PlayerStatisticInGame(models.Model):
    """Модель статистики игрока в конкретной игре"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='+', verbose_name='Матч')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', verbose_name='Игрок')
    accuracy = models.FloatField(default=0, verbose_name='Точность стрельбы')
    headshots_count = models.IntegerField(default=0, verbose_name='Количество убийств в голову')
    kills = models.IntegerField(default=0, verbose_name='Количество убийств')
    deaths = models.IntegerField(default=0, verbose_name='Количество смертей')
