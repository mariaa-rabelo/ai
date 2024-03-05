class ZeroPointOneGame:
    def __init__(self):
        # Initialize an 8x8 game board
        self.board = [[' -- ' for _ in range(8)] for _ in range(8)]
        # Set up the initial positions for red (R) and blue (B) pieces
        self.current_player = 'R'  # Start with Red player
        self.setup_pieces()
        self.capturedPieces = []

    def setup_pieces(self):
        # Blue pieces on the first two rows
        self.board[0] = ['B0-2', 'B0-2', 'B1-1', 'B0-1', 'B1-2', 'B1-1', 'B0-2', 'B0-2']
        self.board[1] = ['B2-2'] * 8  
        
        # Red pieces on the last two rows
        self.board[6] = ['R2-2'] * 8  
        self.board[7] = ['R0-2', 'R0-2', 'R1-1', 'R1-2', 'R0-1', 'R1-1', 'R0-2', 'R0-2']

    # Máximo is mean

    def print_board(self):
        # Print column headers
        print('    ' + '    '.join(str(col) for col in range(8)))
        # Print the current state of the game board with row numbers
        for row_num, row in enumerate(self.board):
            print(str(row_num) + ' ' + ' '.join(row))
        print()
    
    def get_valid_destinations_for_piece(self, piece_row, piece_col, piece):
        destinations = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_destination(piece_row, piece_col, row, col, piece):
                    destinations.append((row, col))
                    print("origin: ", piece_row, piece_col)
                    print("piece: ", piece)
                    print(f"Destination at ({row}, {col}) is valid.")
        return destinations

    def get_player_piece(self):
        # Solicita ao jogador para escolher uma peça para mover
        while True:
            try:
                piece_input = input(f"Player {self.current_player}, enter the coordinates of the piece to move (row, col): ")
                row, col = map(int, piece_input.split(','))
                if self.board[row][col].startswith(self.current_player):
                    return (row, col)
                else:
                    print("That is not your piece. Please choose one of your own pieces.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter coordinates in the format 'row, col'.")

    def get_destination(self, destinations):
        while True:
            try:
                # Prompt the player for the destination coordinates
                dest_input = input("Enter the destination coordinates (row, col): ")
                dest_row, dest_col = map(int, dest_input.split(','))

                # Check if the destination is in the list of valid destinations
                if (dest_row, dest_col) in destinations:
                    return (dest_row, dest_col)
                else:
                    print("Invalid destination. Please choose a valid move.")

            except (ValueError, IndexError):
                # Handle incorrect input formats
                print("Invalid input. Please enter coordinates in the format 'row, col'.")

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
            if destination_piece != ' -- ':
                if destination_piece[0] == piece_owner:
                    return False
                else:
                    # Adiciona a peça capturada à lista de peças capturadas
                    self.capturedPieces.append(destination_piece)
                    return True
            else: # destination_piece == ' -- '
                return True	
        return False  # Retorna False se o tipo de peça não for reconhecido


    def get_player_move(self):
        piece_row, piece_col = self.get_player_piece()
        piece = self.board[piece_row][piece_col]
        destinations = self.get_valid_destinations_for_piece(piece_row, piece_col, piece)
        
        while not destinations:
            print("No valid moves for this piece. Please choose another piece.")
            piece_row, piece_col = self.get_player_piece()
            piece = self.board[piece_row][piece_col]
            destinations = self.get_valid_destinations_for_piece(piece_row, piece_col, piece)

        print(f"Possible destinations for {piece} at ({piece_row}, {piece_col}):")
        for dest in destinations:
            print(dest)
        
        dest_row, dest_col = self.get_destination(destinations)
        return (piece_row, piece_col), (dest_row, dest_col)

    def make_move(self, move):
        (start_row, start_col), (end_row, end_col) = move
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = ' -- '

    #TODO
    def is_terminal(self):
        # returns true if the opponent's 0·1 piece has been captured
        pass

    def evaluate(self):
        # Implement the evaluation heuristic for the board state
        pass

    def get_possible_actions(self):
        # Implement logic to get all possible actions from the current board state
        pass

    def result(self, action):
        # Implement the result of taking an action on the board
        pass

    def minimax(self, depth, maximizing_player):
        if self.is_terminal() or depth == 0:
            return self.evaluate()
        
        if maximizing_player:
            value = float('-inf')
            for action in self.get_possible_actions():
                value = max(value, self.minimax(depth - 1, False))
            return value
        else:
            value = float('inf')
            for action in self.get_possible_actions():
                value = min(value, self.minimax(depth - 1, True))
            return value

    def iterative_deepening_minimax(self, max_depth):
        best_move = None
        best_value = float('-inf') if self.current_player == 'R' else float('inf')
        
        for depth in range(1, max_depth + 1):
            value = self.minimax(depth, self.current_player == 'R')
            if self.current_player == 'R' and value > best_value:
                best_value = value
                # Update best_move with the best action found at this depth
            elif self.current_player == 'B' and value < best_value:
                best_value = value
                # Update best_move with the best action found at this depth     
        return best_move

    def main_menu(self):
        while True:
            print("Welcome to Zero Point One! :)")
            print("1. Play")
            print("2. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.game_loop()
            elif choice == '2':
                print("Exiting the game.")
                break
            else:
                print("Invalid choice, please try again.")

    def game_loop(self):
        while not self.is_terminal():
            self.print_board()
            # check if player wants to exit game
            print("Press 'q' to exit the game, and enter to continue: ")
            choice = input()
            if choice == 'q':
                print("Game over! Player {} exited game!".format(self.current_player))
                return
            move = self.get_player_move()
            self.make_move(move)
            self.current_player = 'B' if self.current_player == 'R' else 'R'  # Switch turns
        print("Game over! Player {} wins!".format(self.current_player))
                

# Create a game instance and print the initial board
if __name__ == "__main__":
    game = ZeroPointOneGame()
    game.main_menu()
