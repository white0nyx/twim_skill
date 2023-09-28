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


class GameMode(models.Model):
    """Модель режима игры"""
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return f'Режим игры: {self.name}_{self.pk}'


class Veto(models.Model):
    """Модель вето"""
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return f'Вето: {self.name}_{self.pk}'


class VetoGameModeInfo(models.Model):
    """Модель, хранящая информацию принадлежности вето к режимам игры"""

    game_mode = models.ForeignKey(GameMode,
                                  on_delete=models.CASCADE,
                                  related_name='veto_game_info',
                                  db_index=False,
                                  null=False, blank=False,
                                  verbose_name='Режим игры')

    veto = models.ForeignKey(Veto,
                             on_delete=models.CASCADE,
                             related_name='veto_game_info',
                             db_index=False,
                             null=False, blank=False,
                             verbose_name='Вето')


class Game(models.Model):
    """Модель матча (игры)"""

    date_start = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала')
    date_end = models.DateTimeField(null=True, verbose_name='Дата окончания')

    map = models.ForeignKey(GameMap,
                            on_delete=models.PROTECT,
                            related_name='game',
                            db_index=True,
                            null=False, blank=False,
                            verbose_name='Карта')

    status = models.ForeignKey(GameStatus,
                               on_delete=models.PROTECT,
                               related_name='game',
                               db_index=True,
                               verbose_name='Статус')

    def __str__(self):
        return f'Игра_{self.pk}'


class PlayerGameInfo(models.Model):
    """Модель записи игрока матча"""

    game = models.ForeignKey(Game,
                             on_delete=models.CASCADE,
                             related_name='player_game_info',
                             db_index=True,
                             null=False, blank=False,
                             verbose_name='Матч')

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='player_game_info',
                             db_index=True,
                             null=False, blank=False,
                             verbose_name='Игрок')

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
