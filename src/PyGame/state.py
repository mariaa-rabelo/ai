import pygame
from constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, BLUE
from piece import Piece

class State:
  def __init__(self):
    self.board = []
    self.create_board()
    self.captured_pieces_blue = []
    self.captured_pieces_blue_curr = [0, 0]
    self.captured_pieces_red = []
    self.captured_pieces_red_curr = [0, 0]
    self.create_captured_pieces_board()

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
    self.remove(piece)
    piece.move(row, col)
    self.board[row][col] = piece

  def remove(self, piece):
    if piece.col < 8:
      self.board[piece.row][piece.col] = 0
    else:
      if piece.row < 4:
        self.captured_pieces_blue[piece.row][piece.col - 8] = 0
      else:
        self.captured_pieces_red[piece.row - 4][piece.col - 8] = 0

  def get_piece(self, row, col):
    return self.board[row][col]
  
  def get_piece_cpb(self, row, col):
    if row < 4:
      return self.captured_pieces_blue[row][col]
    else:
      return self.captured_pieces_red[row - 4][col]

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

  def create_captured_pieces_board(self):
    for row in range(4):
      self.captured_pieces_blue.append([])
      self.captured_pieces_red.append([])
      for _ in range(4):
         self.captured_pieces_blue[row].append(0)
         self.captured_pieces_red[row].append(0)

  def add_captured_piece(self, piece):
    if piece.color == BLUE:
      piece.color = RED
      if self.captured_pieces_red_curr[1] == 3:
        self.captured_pieces_red_curr[0] += 1
        self.captured_pieces_red_curr[1] = 0

      self.captured_pieces_red[self.captured_pieces_red_curr[0]][self.captured_pieces_red_curr[1]] = piece
      piece.move(self.captured_pieces_red_curr[0] + 4, self.captured_pieces_red_curr[1] + 8)
      self.captured_pieces_red_curr[1] += 1

    else:
      piece.color = BLUE
      if self.captured_pieces_blue_curr[1] == 3:
        self.captured_pieces_blue_curr[0] += 1
        self.captured_pieces_blue_curr[1] = 0    

      self.captured_pieces_blue[self.captured_pieces_blue_curr[0]][self.captured_pieces_blue_curr[1]] = piece
      piece.move(self.captured_pieces_blue_curr[0], self.captured_pieces_blue_curr[1] + 8)
      self.captured_pieces_blue_curr[1] += 1

  def draw(self, win):
    self.draw_squares(win)
    for row in range(ROWS):
      for col in range(COLS):
        piece = self.board[row][col]
        if piece != 0:
          piece.draw(win)

    for row in range(ROWS // 2):
      for col in range(COLS, COLS + 4):
        piece = self.captured_pieces_blue[row][col - 8]
        if piece != 0:
          piece.draw(win)

    for row in range(ROWS // 2, ROWS):
      for col in range(COLS, COLS + 4):
        piece = self.captured_pieces_red[row - ROWS // 2][col - 8]
        if piece != 0:
          piece.draw(win)

  def winner(self):
    for row in self.captured_pieces_blue:
      for piece in row:
        if piece != 0 and piece.type == 0.1:
          return True
    for row in self.captured_pieces_red:
      for piece in row:
        if piece != 0 and piece.type == 0.1:
          return True
    return False

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
  
  def get_valid_recovery_positions(self):
        recovery_positions = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    recovery_positions.append((row, col))
        return recovery_positions
