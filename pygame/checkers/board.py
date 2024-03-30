import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, BLUE
from .piece import Piece

class Board:
  def __init__(self):
    self.board = []
    self.create_board()
    self.captured_pieces_blue = []
    self.captured_pieces_blue_curr = (0, 0)
    self.captured_pieces_red = []
    self.captured_pieces_blue_curr = (0, 0)

  def draw_squares(self, win):
    win.fill(WHITE)
    pygame.draw.rect(win, BLACK, (800, 0, 400, 800))
    pygame.draw.rect(win, WHITE, (800, 399, 400, 2))
    for row in range(ROWS):
      for col in range(COLS):
        if col < 2:
          pygame.draw.rect(win, BLUE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif col > 5:
          pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        else:
          pygame.draw.rect(win, BLACK, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE + 1, col*SQUARE_SIZE + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2)) #coords position where to write and dimensions of drawing
    
  def move(self, piece, row, col):
    self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
    piece.move(row, col)

  def remove(self, piece):
    self.board[piece.row][piece.col] = 0

  def get_piece(self, row, col):
    return self.board[row][col]

  def create_board(self):
    for row in range(ROWS):
      self.board.append([])
      for col in range (COLS):
        if row == 1:
          self.board[row].append(Piece(row, col, BLUE, 2.2))
        elif row == 6:
          self.board[row].append(Piece(row, col, RED, 2.2))
        elif row == 0:
          if 0 <= col <= 1 or 6 <= col <= 7:
            self.board[row].append(Piece(row, col, BLUE, 0.2))
          elif col == 2 or col == 5:
            self.board[row].append(Piece(row, col, BLUE, 1.1))
          elif col == 3:
            self.board[row].append(Piece(row, col, BLUE, 0.1))
          else:
            self.board[row].append(Piece(row, col, BLUE, 1.2))
        elif row == 7:
          if 0 <= col <= 1 or 6 <= col <= 7:
            self.board[row].append(Piece(row, col, RED, 0.2))
          elif col == 2 or col == 5:
            self.board[row].append(Piece(row, col, RED, 1.1))
          elif col == 4:
            self.board[row].append(Piece(row, col, RED, 0.1))
          else:
            self.board[row].append(Piece(row, col, RED, 1.2))
        else:
          self.board[row].append(0)

  # def add_captured_piece(self, piece):
  #   if piece.color == BLUE:
  #      if self.captured_pieces_red_curr == (_, 3):
  #         self.captured_pieces_red.append([piece])

  def draw(self, win):
    self.draw_squares(win)
    for row in range(ROWS):
      for col in range(COLS):
        piece = self.board[row][col]
        if piece != 0:
          piece.draw(win)

  def is_valid_destination(self, start_row, start_col, end_row, end_col, piece):
        # Verifica se o destino está dentro do tabuleiro
        if not (0 <= end_row < ROWS and 0 <= end_col < COLS):
            print("Destination is out of bounds.")
            return False
        
        # Dicionário com as funções de validação para cada tipo de peça
        validations = {
            2.2: lambda sr, sc, er, ec: abs(er - sr) == 2 and abs(ec - sc) == 2,
            0.2: lambda sr, sc, er, ec: (abs(er - sr) == 2 and sc == ec) or (sr == er and abs(ec - sc) == 2),
            1.1: lambda sr, sc, er, ec: abs(er - sr) == 1 and abs(ec - sc) == 1,
            1.2: lambda sr, sc, er, ec: (abs(er - sr) == 1 and abs(ec - sc) == 2) or (abs(er - sr) == 2 and abs(ec - sc) == 1),
            0.1: lambda sr, sc, er, ec: (abs(er - sr) == 1 and sc == ec) or (sr == er and abs(ec - sc) == 1),
        }

        destination_piece = self.get_piece(end_row, end_col)

        # Executa a função de validação correspondente ao tipo da peça
        if piece.type not in validations:
            return False
        
        if validations[piece.type](start_row, start_col, end_row, end_col):
            if destination_piece != 0 and destination_piece.color == piece.color:
                return False
            else:
                return True
        return False  # Retorna False se o tipo de peça não for reconhecido

  def get_valid_destinations_for_piece(self, piece_row, piece_col, piece):
        destinations = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.is_valid_destination(piece_row, piece_col, row, col, piece):
                    destinations.append((row, col))
                    # print("origin: ", piece_row, piece_col)
                    # print("piece: ", piece)
                    # print(f"Destination at ({row}, {col}) is valid.")
        return destinations
  
  def get_valid_recovery_positions(self, piece): # remove piece arg
        recovery_positions = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    recovery_positions.append((row, col)) # TODO: check it... is it allowing occupied positions?
        return recovery_positions
  
  def evaluate(self): # TODO: smth better than that kkkkkk
        score = 0
        for row in self.board:
            for cell in row:
                if cell.startswith(self.current_player):
                    score += 1  # Favorável ao jogador atual
                elif cell != ' -- ':
                    score -= 1  # Favorável ao oponente
        return score

  def get_valid_moves(self, piece):
    moves = {}
    left = piece.col - 1
    right = piece.col + 1
    row = piece.row

    if piece.color == RED:
      moves.update(self._traverse_left(row - 1, max(row -3, -1), -1, piece.color, left))
      moves.update(self._traverse_right(row - 1, max(row -3, -1), -1, piece.color, right))

    if piece.color == WHITE:
      moves.update(self._traverse_left(row + 1, min(row +3, -1), 1, piece.color, left))
      moves.update(self._traverse_right(row + 1, min(row +3, -1), 1, piece.color, right))

    return moves

  def _traverse_left(self, start, stop, step, color, left, skipped = []):
    moves = {}
    last = []
    for r in range(start, stop, step):
      if left < 0:
        break

      current = self.board[r][left]
      if current == 0:
        if skipped and not last:
          break
        elif skipped:
          moves[(r, left)] = last + skipped
        else:
          moves[(r, left)] = last

        if last:
          if step == -1:
            row = max(r-3, -1)
          else:
            row = min(r+3, ROWS)

          moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped = last))
          moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped = last))
        break

      elif current.color == color:
        break
      else:
        last = [current]

      left -= 1

    return moves

  def _traverse_right(self, start, stop, step, color, right, skipped = []):
    moves = {}
    last = []
    for r in range(start, stop, step):
      if right >= COLS:
        break

      current = self.board[r][right]
      if current == 0:
        if skipped and not last:
          break
        elif skipped:
          moves[(r, right)] = last + skipped
        else:
          moves[(r, right)] = last

        if last:
          if step == -1:
            row = max(r-3, -1)
          else:
            row = min(r+3, ROWS)

          moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped = last))
          moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped = last))
          break

      elif current.color == color:
        break
      else:
        last = [current]

      right += 1

    return moves