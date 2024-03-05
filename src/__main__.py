class ZeroPointOneGame:
    def __init__(self):
        # Initialize an 8x8 game board
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        # Set up the initial positions for red (R) and blue (B) pieces
        self.game_over = False
        self.current_player = 'R'  # Start with Red player
        self.setup_pieces()

    def setup_pieces(self):
        # Red pieces on the first two rows
        for i in range(2):
            for j in range(8):
                self.board[i][j] = 'R'
        # Blue pieces on the last two rows
        for i in range(6, 8):
            for j in range(8):
                self.board[i][j] = 'B'

    def print_board(self):
        # Print the current state of the game board
        for row in self.board:
            print(' '.join(row))
        print()

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

    def get_destination(self, piece_row, piece_col):
        # Solicita ao jogador para escolher uma posição de destino válida
        while True:
            try:
                dest_input = input("Enter the destination coordinates (row, col): ")
                dest_row, dest_col = map(int, dest_input.split(','))
                if self.is_valid_destination(piece_row, piece_col, dest_row, dest_col):
                    return (dest_row, dest_col)
                else:
                    print("Invalid destination. Please choose a valid move.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter coordinates in the format 'row, col'.")

    def is_valid_destination(self, piece_row, piece_col, dest_row, dest_col):
        # TODO: validate for each piece type
        return 0 <= dest_row < 8 and 0 <= dest_col < 8 and self.board[dest_row][dest_col] == '.'

    def get_player_move(self):
        piece_row, piece_col = self.get_player_piece()
        dest_row, dest_col = self.get_destination(piece_row, piece_col)
        return (piece_row, piece_col), (dest_row, dest_col)

    def make_move(self, move):
        (start_row, start_col), (end_row, end_col) = move
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = '.'

    #TODO
    def is_terminal(self):
        # Implement the logic to check if the game is over
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
        while not self.game_over:
            self.print_board()
            move = self.get_player_move()
            self.make_move(move)
            self.current_player = 'B' if self.current_player == 'R' else 'R'  # Switch turns
            # Check for game over condition
            self.game_over = self.is_terminal()
            if self.game_over:
                print("Game over! Player {} wins!".format(self.current_player))
                break

# Create a game instance and print the initial board
if __name__ == "__main__":
    game = ZeroPointOneGame()
    game.main_menu()
