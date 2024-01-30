from datetime import timezone
from django.utils import timezone
from django.db import models
from django.template.defaultfilters import slugify

from games.models import GameType, GameMode, Veto, Pool, Map, Match
from users.models import User


class Lobby(models.Model):
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader', verbose_name='Лидер')
    map = models.ForeignKey(Map, on_delete=models.PROTECT, max_length=255, verbose_name='Карта')
    pool = models.ForeignKey(Pool, on_delete=models.PROTECT, related_name='+', verbose_name='Пул')
    bet = models.IntegerField(default=0, verbose_name='Ставка')
    password_lobby = models.CharField(max_length=255, null=True, verbose_name='Пароль')
    max_lvl_enter = models.IntegerField(null=True, verbose_name='Максимальный уровень для входа')
    min_lvl_enter = models.IntegerField(null=True, verbose_name='Минимальный уровень для входа')
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name='SLUG')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='lobby', verbose_name='Матч')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.map}-{timezone.now().strftime('%Y%m%d%H%M%S')}")
        super(Lobby, self).save(*args, **kwargs)


class PlayerLobby(models.Model):
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='lobby')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    time_enter = models.DateTimeField(auto_now=True, verbose_name='Время входа')
    team_id = models.IntegerField()
    in_lobby = models.BooleanField()
