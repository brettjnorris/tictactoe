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

  def serialize_board(self):
    current_board = json.loads(self.board)
    for move in self.move_set.all():
      print "%s %s" % (move.position, move.player_type)
      current_board[ str(move.position) ] = move.player_type

    return json.dumps(current_board) 

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
    else:
      self.board = self.serialize_board()

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

  def save(self, *args, **kwargs):
    # If the related Game is finished, don't allow the Move to be saved
    if self.game.game_state is not constants.STATE_INPROGRESS:
      return False

    # Update the related Game object when a new Move is created
    if not self.pk:
      self.game.save()

    super(Move, self).save(*args, **kwargs) 

  def __unicode__(self):
    return "Game #%s - %s selects %d at %s" % (self.game.pk, self.get_player_type_display(), self.position, self.created)