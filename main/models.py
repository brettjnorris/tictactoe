from django.db import models
import json
import constants

class Game(models.Model):
  GAME_STATES = (
    (constants.STATE_INPROGRESS, 'In Progress'),
    (constants.STATE_DRAW, 'Draw'),
    (constants.STATE_PLAYERWON, 'Player Won'),
    (constants.STATE_CPUWON, 'CPU Won'),
  ) 

  board = models.TextField(blank=True)
  player_name = models.CharField(max_length=50, default="Player 1")
  game_state = models.IntegerField(choices=GAME_STATES, blank=True)
  created = models.DateTimeField(auto_now_add=True)

  def save(self, *args, **kwargs):
    if not self.pk:
      newboard = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
      }

      self.board = json.dumps(newboard)
      self.game_state = constants.STATE_INPROGRESS
      super(Game, self).save(*args, **kwargs)

  def __unicode__(self):
    return "Game #%s vs %s started at %s" % (self.pk, self.player_name, self.created)


class Move(models.Model):
  PLAYER_TYPES = (
    (constants.PLAYER, 'Player'),
    (constants.CPU, 'CPU'),
  )

  player_type = models.CharField(max_length=1, choices=PLAYER_TYPES)
  position = models.IntegerField()
  created = models.DateTimeField(auto_now_add=True)
  game = models.ForeignKey('Game')

  def __unicode__(self):
    return "Game #%s - %s selects %d at %s" % (self.game.pk, self.get_player_type_display(), self.position, self.created)