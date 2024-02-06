from rest_framework import serializers

from games.models import Game, Match


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('date_start', 'date_end', 'map', 'status', 'match')


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('pk', 'type', 'mode', 'veto')
