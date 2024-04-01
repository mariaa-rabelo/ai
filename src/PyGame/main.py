import pygame
from constants import WIDTH, HEIGHT, SQUARE_SIZE, BLUE
from game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Zero.One')

def get_row_col_from_mouse(pos):
  x, y = pos
  row = y // SQUARE_SIZE
  col = x // SQUARE_SIZE
  return row, col

def main():
  run = True
  clock = pygame.time.Clock()
  game = Game(WIN)

  while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = get_row_col_from_mouse(pos)
        if col < 8:
          game.select(row, col)
        else:
          game.select_cpb(row, col - 8)
    
    game.update()
    if game.winner():
      run = False        
      winner = 'Red' if game.turn == BLUE else 'Blue' 
      print("Game over! Player {} wins!".format(winner))
      print("Total turns: ", game.turns_count)

  pygame.quit()

main()