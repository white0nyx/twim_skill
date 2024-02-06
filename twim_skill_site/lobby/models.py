from datetime import timezone
from django.utils import timezone
from django.db import models
from django.template.defaultfilters import slugify

from games.models import GameType, GameMode, Veto, Pool, Map, Match
from users.models import User


class Lobby(models.Model):
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader', verbose_name='Лидер')
    password_lobby = models.CharField(max_length=255, null=True, verbose_name='Пароль')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='lobby', verbose_name='Матч')


class PlayerLobby(models.Model):
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='lobby')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    time_enter = models.DateTimeField(auto_now=True, verbose_name='Время входа')
