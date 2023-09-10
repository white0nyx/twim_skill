from datetime import timezone
from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.conf import settings

from twim_skill_site import settings


# class User(models.Model):
#     nickname = models.CharField(max_length=255)
#     id_role = models.IntegerField()
#     registration_date = models.DateField()
#     last_enter_date = models.DateField()
#     steam_url = models.CharField(max_length=255)
#     faciet_url = models.CharField(max_length=255)


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

class PlayersLobby(models.Model):
    id_lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='players')
    id_user = models.IntegerField()
    team_id = models.IntegerField()
    in_lobby = models.BooleanField()