from django.db import models

from users.models import User


class Map(models.Model):
    """Модель карты игры"""
    name = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='images/maps_images')

    def __str__(self):
        return f'Карта: {self.name}_{self.pk}'


class PoolGroup(models.Model):
    """Модель группы пула карт"""
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return f'Группа пулов: {self.name}_{self.pk}'


class Pool(models.Model):
    """Модель пула карт"""
    name = models.CharField(max_length=255, verbose_name='Название')
    pool_group = models.ForeignKey(PoolGroup,
                                   on_delete=models.PROTECT,
                                   related_name='pool',
                                   db_index=False,
                                   null=False, blank=False,
                                   verbose_name='Группа')


class PoolMapInfo(models.Model):
    """Модель связи пула и карты"""
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name='+', verbose_name='Пул')
    map = models.ForeignKey(Map, on_delete=models.CASCADE, related_name='+', verbose_name='Карта')


class GameType(models.Model):
    """Модель типа игры"""
    name = models.CharField(max_length=255, verbose_name='Название')
    quantity_players = models.PositiveSmallIntegerField(verbose_name='Количество игроков', unique=True)

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
    """Модель игры"""

    date_start = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала')
    date_end = models.DateTimeField(null=True, verbose_name='Дата окончания')

    map = models.ForeignKey(Map,
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


class PlayerStatisticInGame(models.Model):
    """Модель статистики игрока в конкретной игре"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='+', verbose_name='Игра')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', verbose_name='Игрок')
    kills = models.IntegerField(default=0, verbose_name='Количество убийств')
    assists = models.IntegerField(default=0, verbose_name='Количество помощи')
    deaths = models.IntegerField(default=0, verbose_name='Количество смертей')
    headshots_count = models.IntegerField(default=0, verbose_name='Количество убийств в голову')
    kr_ratio = models.FloatField(default=0, verbose_name='K/R')
    mvp = models.PositiveSmallIntegerField(default=0, verbose_name='MVP')
    triple_kills = models.PositiveSmallIntegerField(default=0, verbose_name='Количество тройных убийств')
    quadro_kills = models.PositiveSmallIntegerField(default=0, verbose_name='Количество четверных убийств')
    five_kills = models.PositiveSmallIntegerField(default=0, verbose_name='Количество пятерных убийств')


# <------------------ МАТЧИ ------------------>

# Исправить везде on_delete и related_name
class Match(models.Model):
    """Модель матча"""
    game1 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='+', verbose_name='Игра 1')
    game2 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='+', verbose_name='Игра 2')
    game3 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='+', verbose_name='Игра 3')
    game4 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='+', verbose_name='Игра 4')
    game5 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='+', verbose_name='Игра 5')
    mode = models.ForeignKey(GameMode, on_delete=models.PROTECT, related_name='+', verbose_name='Режим BEST_OF')
    veto = models.ForeignKey(Veto, on_delete=models.PROTECT, related_name='+', verbose_name='Вето')


class PlayerMatchInfo(models.Model):
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

    is_win = models.BooleanField(verbose_name='Победа')

    def __str__(self):
        return f'Информация_{self.pk} о user_{self.user.pk} в игре {self.game.pk}'
