from django.shortcuts import render
from rest_framework import generics

from games.models import Game, Match
from games.serializers import GameSerializer, MatchSerializer


class GameAPIList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameAPIUpdate(generics.UpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class MatchAPIList(generics.ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
