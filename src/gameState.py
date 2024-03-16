class GameState:
    def __init__(self, board, current_player, capturedPieces):
        self.board = board
        self.current_player = current_player
        self.capturedPieces = capturedPieces
        self.setup_pieces()

    def setup_pieces(self):
        # Blue pieces on the first two rows
        self.board[0] = ['B0-2', 'B0-2', 'B1-1', 'B0-1', 'B1-2', 'B1-1', 'B0-2', 'B0-2']
        self.board[1] = ['B2-2'] * 8  
        
        # Red pieces on the last two rows
        self.board[6] = ['R2-2'] * 8  
        self.board[7] = ['R0-2', 'R0-2', 'R1-1', 'R1-2', 'R0-1', 'R1-1', 'R0-2', 'R0-2']

    def is_valid_destination(self, start_row, start_col, end_row, end_col, piece):
        # Verifica se o destino está dentro do tabuleiro
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            print("Destination is out of bounds.")
            return False
        
        # Dicionário com as funções de validação para cada tipo de peça
        validations = {
            '2-2': lambda sr, sc, er, ec: abs(er - sr) == 2 and abs(ec - sc) == 2,
            '0-2': lambda sr, sc, er, ec: (abs(er - sr) == 2 and sc == ec) or (sr == er and abs(ec - sc) == 2),
            '1-1': lambda sr, sc, er, ec: abs(er - sr) == 1 and abs(ec - sc) == 1,
            '1-2': lambda sr, sc, er, ec: (abs(er - sr) == 1 and abs(ec - sc) == 2) or (abs(er - sr) == 2 and abs(ec - sc) == 1),
            '0-1': lambda sr, sc, er, ec: (abs(er - sr) == 1 and sc == ec) or (sr == er and abs(ec - sc) == 1),
        }

        piece_owner = piece[0]  # 'R' or 'B'
        piece_type = piece[1:]  # '1-1', '0-2', etc.

        destination_piece = self.board[end_row][end_col]

        # Executa a função de validação correspondente ao tipo da peça
        if piece_type not in validations:
            return False
        
        if validations[piece_type](start_row, start_col, end_row, end_col):
            if destination_piece[0] == piece_owner:
                return False
            else:
                return True
        return False  # Retorna False se o tipo de peça não for reconhecido

    def get_valid_destinations_for_piece(self, piece_row, piece_col, piece):
        destinations = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_destination(piece_row, piece_col, row, col, piece):
                    destinations.append((row, col))
                    # print("origin: ", piece_row, piece_col)
                    # print("piece: ", piece)
                    # print(f"Destination at ({row}, {col}) is valid.")
        return destinations

    def is_terminal(self):
        if 'R0-1' in self.capturedPieces or 'B0-1' in self.capturedPieces:
            return True
        return False

    # TODO : confirm itt
    def evaluate(self):
        # Initialize scores for both players
        score_red, score_blue = 0, 0

        # Iterate through the board to count pieces
        for row in self.board:
            for cell in row:
                if cell.startswith('R'):  # Piece belongs to the Red player
                    score_red += 1
                elif cell.startswith('B'):  # Piece belongs to the Blue player
                    score_blue += 1

        # Return the score for the current player and subtract the opponent's score
        # This assumes the current player is maximizing their score
        if self.current_player == 'R':
            return score_red - score_blue
        else:
            return score_blue - score_red

    def make_move(self, move):
        (start_row, start_col), (end_row, end_col) = move
        if self.board[end_row][end_col] != ' -- ':
            print("Player {} captured {} piece!".format(self.current_player, self.board[end_row][end_col]))
            self.capturedPieces.append(self.board[end_row][end_col])
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = ' -- '

    def recover_piece(self, recovery):
        choosen_piece, (dest_row, dest_col) = recovery
        for piece in self.capturedPieces:
            if piece == choosen_piece:
                self.capturedPieces.remove(piece)
                break
        # transform the opponent piece into a current player piece
        new_piece = self.current_player + choosen_piece[1:]
        self.board[dest_row][dest_col] = new_piece
        return
      
