import pygame

# width and height of the pygame window
WIDTH, HEIGHT = 1200, 800
# number of rows and columns in the board
ROWS, COLS = 8, 8
# size of each square
SQUARE_SIZE = 100

#rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)

# load images
ZEROONE = pygame.image.load('../../assets/0.1.png')
ZEROTWO = pygame.image.load('../../assets/0.2.png')
ONEONE = pygame.image.load('../../assets/1.1.png')
ONETWO = pygame.image.load('../../assets/1.2.png')
TWOONE = pygame.image.load('../../assets/2.1.png')
TWOTWO = pygame.image.load('../../assets/2.2.png')
