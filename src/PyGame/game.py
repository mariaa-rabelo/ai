import pygame
from constants import RED, GREEN, BLUE, SQUARE_SIZE
from state import State

class Game:
  """
  Class to manage the game logic.
  """
  def __init__(self, win):
    self._init()
    # pygame window
    self.win = win

  # update the screen
  def update(self):
    self.board.draw(self.win)
    self.draw_valid_moves(self.valid_moves)
    pygame.display.update()

  def _init(self):
    # selected piece starts at None
    self.selected = None
    # initialize board
    self.board = State()
    # first player is Red
    self.turn = RED
    self.turns_count = 0
    # valid moves for selected piece
    self.valid_moves = []

  def reset(self):
    self._init()

  # returns True if there's a winner, otherwise False
  def winner(self):
    return self.board.winner()

  """
  Selects a piece based on the coordinates of the mouse click.
  If there's already a selected piece, performs a move to the specified coordinates
  """
  def select(self, row, col):
    # If there's a selected piece
    if self.selected:
      self._move(row, col)

    # Selects piece and get valid destinations to draw on the screen
    piece = self.board.get_piece(row, col)
    if piece != 0 and piece.color == self.turn:
      self.selected = piece
      self.valid_moves = self.board.get_valid_destinations_for_piece(row, col, piece)
      return True
    
    return False
  
  """
  Selects a piece in the captured pieces board.
  Since you can't perform moves into the captured pieces board, it only selectes pieces and doesn't perform moves.
  """
  def select_cpb(self, row, col):
    piece = self.board.get_piece_cpb(row, col)
    if piece != 0 and piece.color == self.turn:
      self.selected = piece
      self.valid_moves = self.board.get_valid_recovery_positions()
      return True
    
    return False

  # Function to handle piece movement
  def _move(self, row, col):
    piece = self.board.get_piece(row, col)  # Getting the piece at the specified coordinates
    if self.selected and piece == 0 and (row, col) in self.valid_moves:  # If a piece is selected, destination is empty, and move is valid
      self.board.move(self.selected, row, col)  # Moving the piece
      self.valid_moves = []  # Clearing valid moves
      self.selected = None  # Deselecting the piece
      self.change_turn()  # Changing the turn
    elif self.selected and piece != 0 and (row, col) in self.valid_moves:  # If a piece is selected, destination has opponent's piece, and move is valid
      self.board.remove(piece)  # Removing opponent's piece
      self.board.add_captured_piece(piece)  # Adding captured piece to the captured pieces board
      self.board.move(self.selected, row, col)  # Moving the piece
      self.valid_moves = []  # Clearing valid moves
      self.selected = None  # Deselecting the piece
      self.change_turn()  # Changing the turn
    else:
      return False  # Returning False if the move is invalid
    
    return True  # Returning True to indicate successful move
  
  # Function to draw valid moves on the board
  def draw_valid_moves(self, moves):
    for move in moves:
      row, col = move
      pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

  # Function to change turns
  def change_turn(self):
    self.turns_count += 1
    if self.turn == RED:
      self.turn = BLUE

    else:
      self.turn = RED
