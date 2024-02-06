from django.shortcuts import render
from rest_framework import generics

from games.models import Game, Match
from games.serializers import GameSerializer, MatchSerializer


class GameAPIView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class MatchAPIView(generics.ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
