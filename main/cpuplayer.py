import json
import constants

class CPUPlayer(object):
  ROWS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
  )

  PRIORITIES = (
    4, 
    (0, 2, 6, 8),
    (1, 3, 5, 7),
  )

  ROW_POINTS = { 0: 0, 1: 10, 2: 100, 3: 1000 }

  def __init__(self, board):
    self.boardstate = self.parse_board(board)

  def parse_board(self, board):
    """
    Returns dict representing given board from json
    """
    if type(board) is str:
      return json.loads(board)

    return board

  def serialize_board(self, board):
    """
    Returns json string representing given board from dict
    """
    if type(board) is not str:
      return json.dumps(board)

    return board

  def has_won(self, board):
    """
    Returns value of winning player or false if not yet won
    """
    for row in self.ROWS:
      if (board[str(row[0])] != 0) and (board[str(row[0])] == board[str(row[1])] == board[str(row[2])]):
        return board[str(row[0])]

    return False

  def get_possible_moves(self, board):
    """
    Returns list of possible moves for given board

    """
    moves = []
    for i in board:
      if board[i] == 0:
        moves.append(i)

    return moves

  def score(self, board):
    """
    Returns int

    Score is calculated as a sum of each winnable row based on the following rules:

    10   Points for 1 move
    100  Points for 2 moves
    1000 Points for 3 moves

    Opponent moves get a negative score.

    """
    score = 0

    for row in self.ROWS:
      player_count = 0
      cpu_count = 0

      for tile in row:
        if board[str(tile)] == constants.PLAYER:
          player_count += 1

        if board[str(tile)] == constants.CPU:
          cpu_count += 1


      score += (self.ROW_POINTS[cpu_count] - self.ROW_POINTS[player_count])

    return score

  def get_best_move(self):
    """
    Returns best possible move using the minimax recursive algorithm
    """
    board = self.boardstate.copy()
    possible_moves = self.get_possible_moves(board)

    best_move = -1
    best_score = float('-inf')

    for move in possible_moves:
      board[str(move)] = constants.CPU
      score = self.minimax(len(possible_moves) - 1, board, constants.PLAYER)

      if score > best_score:
        best_score = score
        best_move = move

      board[str(move)] = 0

    return best_move

  def minimax(self, level, board, player):
    """
    Recursively determine the best move by scoring each possible move given a board state

    CPU's moves are maximized (find the best score)
    Player's moves are minimized (assume the worst move possible)

    """
    possible_moves = self.get_possible_moves(board)
    if level == 0 or self.has_won(board):
      return self.score(board)


    # maximizing player
    if player == constants.CPU:
      best_score = float('-inf')

      for move in possible_moves:
        board[str(move)] = player
        score = self.minimax(level - 1, board, constants.PLAYER)

        if score > best_score:
          best_score = score
          best_move = move

        board[str(move)] = 0

    # minimizing player
    if player == constants.PLAYER:
      best_score = float('inf')

      for move in possible_moves:
        board[str(move)] = player
        score = self.minimax(level - 1, board, constants.CPU)

        if score < best_score:
          best_score = score
          best_move = move

        board[str(move)] = 0

    return best_score

   







