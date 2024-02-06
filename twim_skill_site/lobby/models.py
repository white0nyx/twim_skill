from datetime import timezone
from django.utils import timezone
from django.db import models
from django.template.defaultfilters import slugify

from games.models import Match
from users.models import User


class Lobby(models.Model):
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader', verbose_name='Лидер')
    bet = models.IntegerField(default=0, verbose_name='Ставка')
    password_lobby = models.CharField(max_length=255, null=True, verbose_name='Пароль')
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
