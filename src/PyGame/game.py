import pygame
from constants import RED, GREEN, BLUE, SQUARE_SIZE
from state import State

class Game:
  def __init__(self, win):
    self._init()
    self.win = win

  def update(self):
    self.board.draw(self.win)
    self.draw_valid_moves(self.valid_moves)
    pygame.display.update()

  def _init(self):
    self.selected = None
    self.board = State()
    self.turn = RED
    self.turns_count = 0
    self.valid_moves = []

  def reset(self):
    self._init()

  def winner(self):
    return self.board.winner()

  def select(self, row, col):
    if self.selected:
      self._move(row, col)

    piece = self.board.get_piece(row, col)
    if piece != 0 and piece.color == self.turn:
      self.selected = piece
      self.valid_moves = self.board.get_valid_destinations_for_piece(row, col, piece)
      return True
    
    return False
  
  def select_cpb(self, row, col):
    piece = self.board.get_piece_cpb(row, col)
    if piece != 0 and piece.color == self.turn:
      self.selected = piece
      self.valid_moves = self.board.get_valid_recovery_positions()
      return True
    
    return False

  def _move(self, row, col):
    piece = self.board.get_piece(row, col)
    if self.selected and piece == 0 and (row, col) in self.valid_moves:
      self.board.move(self.selected, row, col)
      self.valid_moves = []
      self.selected = None
      self.change_turn()
    elif self.selected and piece != 0 and (row, col) in self.valid_moves:
      self.board.remove(piece)
      self.board.add_captured_piece(piece)
      self.board.move(self.selected, row, col)
      self.valid_moves = []
      self.selected = None
      self.change_turn()
    else:
      return False
    
    return True
  
  def draw_valid_moves(self, moves):
    for move in moves:
      row, col = move
      pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

  def change_turn(self):
    self.turns_count += 1
    if self.turn == RED:
      self.turn = BLUE

    else:
      self.turn = RED
