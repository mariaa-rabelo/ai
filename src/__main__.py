class ZeroPointOneGame:
    def __init__(self):
        # Initialize an 8x8 game board
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        # Set up the initial positions for red (R) and blue (B) pieces
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



# Create a game instance and print the initial board
game = ZeroPointOneGame()
game.print_board()
