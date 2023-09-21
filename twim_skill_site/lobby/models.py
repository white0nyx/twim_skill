from datetime import timezone
from django.utils import timezone
from django.db import models
from django.template.defaultfilters import slugify


class Lobby(models.Model):
    id_leader = models.IntegerField()
    map = models.CharField(max_length=255)
    bet = models.IntegerField()
    password_lobby = models.IntegerField()
    max_lvl_enter = models.IntegerField()
    deleted = models.BooleanField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.map}-{timezone.now().strftime('%Y%m%d%H%M%S')}")
        super(Lobby, self).save(*args, **kwargs)


class PlayerLobby(models.Model):
    id_lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='players')
    id_user = models.IntegerField()
    team_id = models.IntegerField()
    in_lobby = models.BooleanField()
