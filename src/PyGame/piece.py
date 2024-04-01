import pygame
from constants import *

class Piece:
  PADDING = 15
  OUTLINE = 2

  def __init__(self, row, col, color, type):
    # Initializing piece attributes
    self.row = row
    self.col = col
    self.color = color
    self.type = type

    self.x = 0
    self.y = 0
    self.calc_pos()  # Calculating the position of the piece on the board

  # Function to calculate the position of the piece on the board
  def calc_pos(self):
    self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
    self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

  # Function to draw the piece on the board
  def draw(self, win):
    radius = SQUARE_SIZE // 2 - self.PADDING
    # Drawing the piece with a circle outline
    pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
    pygame.draw.circle(win, self.color,(self.x, self.y), radius)
    # Drawing the piece type
    if self.type == 0.1:
      win.blit(ZEROONE, (self.x - ZEROONE.get_width() // 2, self.y - ZEROONE.get_height() // 2))
    elif self.type == 0.2:
      win.blit(ZEROTWO, (self.x - ZEROTWO.get_width() // 2, self.y - ZEROTWO.get_height() // 2))
    elif self.type == 1.1:
      win.blit(ONEONE, (self.x - ONEONE.get_width() // 2, self.y - ONEONE.get_height() // 2))
    elif self.type == 1.2:
      win.blit(ONETWO, (self.x - ONETWO.get_width() // 2, self.y - ONETWO.get_height() // 2))
    elif self.type == 2.1:
      win.blit(TWOONE, (self.x - TWOONE.get_width() // 2, self.y - TWOONE.get_height() // 2))
    elif self.type == 2.2:
      win.blit(TWOTWO, (self.x - TWOTWO.get_width() // 2, self.y - TWOTWO.get_height() // 2))
  
  # Function to move the piece to a new position
  def move(self, row, col):
    self.row = row
    self.col = col
    self.calc_pos()  # Recalculating the position of the piece

  # Function to represent the piece as a string
  def __repr__(self):
    return str(self.color)
