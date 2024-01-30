from rest_framework import serializers

from lobby.models import Lobby


class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = ('leader', 'map', 'min_lvl_enter', 'max_lvl_enter', 'match')