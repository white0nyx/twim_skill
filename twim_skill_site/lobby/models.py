from datetime import timezone
from django.utils import timezone
from django.db import models
from django.template.defaultfilters import slugify

from users.models import User

class Lobby(models.Model):
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader')
    map = models.CharField(max_length=255)
    bet = models.IntegerField()
    password_lobby = models.CharField(max_length=255, null=True)
    max_lvl_enter = models.IntegerField(null=True)
    min_lvl_enter = models.IntegerField(null=True)
    deleted = models.BooleanField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.map}-{timezone.now().strftime('%Y%m%d%H%M%S')}")
        super(Lobby, self).save(*args, **kwargs)


class PlayerLobby(models.Model):
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='lobby')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    team_id = models.IntegerField()
    in_lobby = models.BooleanField()
