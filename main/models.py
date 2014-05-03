from django.db import models
import json
import constants
from cpuplayer import CPUPlayer

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
      current_board[ str(move.position) ] = move.player_type

    return json.dumps(current_board) 

  def check_game_state(self):
    # Check for draw
    current_board = json.loads(self.board)

    open_moves = 0
    for i in range(0, 9):
      if current_board[str(i)] == 0:
        open_moves += 1

    if open_moves == 0:
      return constants.STATE_DRAW

    player = CPUPlayer(current_board)
    winner = player.has_won(current_board)

    if winner == constants.PLAYER:
      return constants.STATE_PLAYERWON
    elif winner == constants.CPU:
      return constants.STATE_CPUWON

    return constants.STATE_INPROGRESS

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
      self.game_state = self.check_game_state()

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

  def generate_cpu_move(self):
    player = CPUPlayer(self.game.board)
    return int(player.get_best_move())

  def save(self, *args, **kwargs):
    print self.game.game_state
    # If the related Game is finished, don't allow the Move to be saved
    if self.game.game_state is not constants.STATE_INPROGRESS:
      return False

    super(Move, self).save(*args, **kwargs) 

    # Save the related game object after we've updated
    self.game.save()

    # If it's the CPU's turn, generate that play 
    if self.game.game_state == constants.STATE_INPROGRESS and self.player_type == constants.PLAYER:
      cpu_move = Move()
      cpu_move.player_type = constants.CPU
      cpu_move.position = self.generate_cpu_move()
      cpu_move.game = Game.objects.get(pk=self.game.pk)
      cpu_move.save()

  def __unicode__(self):
    return "Game #%s - %s selects %d at %s" % (self.game.pk, self.get_player_type_display(), self.position, self.created)