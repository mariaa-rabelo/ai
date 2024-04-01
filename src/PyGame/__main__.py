import pygame
from constants import WIDTH, HEIGHT, SQUARE_SIZE, BLUE
from game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Zero.One')

def get_row_col_from_mouse(pos):
  """
  Function to get board coordinates (row, col) based on mouse position
  
  Args:
      pos [int, int]: coordinates of the mouse
      
  Returns:
      row, col [int, int]: board coordinates of the mouse
  """
  x, y = pos
  row = y // SQUARE_SIZE
  col = x // SQUARE_SIZE
  return row, col

def main():
  """
  Main game loop that runs continuously to update the screen, handle mouse clicks and check for winners
  """
  run = True
  clock = pygame.time.Clock()
  game = Game(WIN)

  while run:
    clock.tick(FPS)
    
    # if you click the exit window button, quit
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      # if you click the board, get coordinates
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = get_row_col_from_mouse(pos)
        # if you click the board, call game.select
        if col < 8:
          game.select(row, col)
        # if you click outside the board, you're clicking the captured pieces part of the window, call game.select_cpb
        else:
          game.select_cpb(row, col - 8)
    
    # update screen
    game.update()
    # if there's a winner, stop the game and print the victor in the terminal
    if game.winner():
      run = False        
      winner = 'Red' if game.turn == BLUE else 'Blue' 
      print("Game over! Player {} wins!".format(winner))
      print("Total turns: ", game.turns_count)

  pygame.quit()

# Check if the script is run directly (and not imported)
if __name__ == "__main__":
    # If this script is run as the main program, call the main function
    main()