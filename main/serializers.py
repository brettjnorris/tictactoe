from main.models import Game, Move
from rest_framework import serializers

class MoveSerializer(serializers.ModelSerializer):
  class Meta:
    model = Move
    fields = ('id', 'game', 'position')


class GameSerializer(serializers.ModelSerializer):
  moves = MoveSerializer(many=True)

  class Meta:
    model = Game
    fields = ('id', 'board', 'player_name', 'game_state')