from django.shortcuts import render
from rest_framework import viewsets
from main.models import Game, Move
from main.serializers import GameSerializer, MoveSerializer

class MoveViewSet(viewsets.ModelViewSet):
  queryset = Move.objects.all()
  serializer_class = MoveSerializer

class GameViewSet(viewsets.ModelViewSet):
  queryset = Game.objects.all()
  serializer_class = GameSerializer
