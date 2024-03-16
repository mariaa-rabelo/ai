from gameState import GameState

class ZeroPointOneGame:
    def __init__(self):
        self.state = GameState(
            board=[[' -- ' for _ in range(8)] for _ in range(8)],
            current_player='R',
            capturedPieces=['B2-2', 'R1-2']
        )

    # Máximo is mean

    def print_board(self):
        print('    ' + '    '.join(str(col) for col in range(8)))
        for row_num, row in enumerate(self.state.board):
            print(str(row_num) + ' ' + ' '.join(row))
        print()
        print("Captured pieces: ", self.state.capturedPieces)
    
    def get_player_piece(self):
        # Solicita ao jogador para escolher uma peça para mover
        while True:
            try:
                piece_input = input(f"Player {self.state.current_player}, enter the coordinates of the piece to move (row, col): ")
                row, col = map(int, piece_input.split(','))
                if self.state.board[row][col].startswith(self.state.current_player):
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
    
    def get_player_move(self):
        piece_row, piece_col = self.get_player_piece()
        piece = self.state.board[piece_row][piece_col]
        destinations = self.state.get_valid_destinations_for_piece(piece_row, piece_col, piece)
        
        while not destinations:
            print("No valid moves for this piece. Please choose another piece.")
            piece_row, piece_col = self.get_player_piece()
            piece = self.state.board[piece_row][piece_col]
            destinations = self.state.get_valid_destinations_for_piece(piece_row, piece_col, piece)

        print(f"Possible destinations for {piece} at ({piece_row}, {piece_col}):")
        for dest in destinations:
            print(dest)
        
        dest_row, dest_col = self.get_destination(destinations)
        return (piece_row, piece_col), (dest_row, dest_col)
    

    def get_recovery(self): # recover = (piece_type, row, col)
        piece = self.choose_captured_piece()

        # change it to work both for captured pieces and in-board pieces
        # destinations = self.state.get_valid_destinations_for_piece(piece)

        # print(f"Possible destinations for {piece} at ({piece_row}, {piece_col}):")
        # for dest in destinations:
        #     print(dest)
        
       # dest_row, dest_col = self.get_destination(destinations)
        dest_row, dest_col = self.get_recovery_destination()
        return piece, (dest_row, dest_col)

    def choose_captured_piece(self):
        while True:
            if self.state.current_player == 'R':
                print("Choose a black piece to recover:")
                for i, piece in enumerate(self.state.capturedPieces):
                    if piece.startswith('B'):
                        print(f"{i+1}. {piece}")
            else:
                print("Choose a red piece to recover:")
                for i, piece in enumerate(self.state.capturedPieces):
                    if piece.startswith('R'):
                        print(f"{i+1}. {piece}")
                        
            choice = input("Enter your choice: ")
            if choice.isdigit():
                if 0 < int(choice) <= len(self.state.capturedPieces):
                    return self.state.capturedPieces[int(choice) - 1]
                else:
                    print("Invalid choice, please select one of the possible numbers.")
            else:
                print("Invalid input, please enter a number.")

    def get_recovery_destination(self):
        while True:
            try:
                # Prompt the player for the destination coordinates
                dest_input = input("Enter the destination coordinates (row, col): ")
                dest_row, dest_col = map(int, dest_input.split(','))

                # Check if the destination is in the list of valid destinations
                if self.state.board[dest_row][dest_col] == ' -- ':
                    return (dest_row, dest_col)
                else:
                    print("Invalid destination. Please choose an empty cell.")

            except (ValueError, IndexError):
                # Handle incorrect input formats
                print("Invalid input. Please enter coordinates in the format 'row, col'.")
                
    def minimax(self, depth, maximizing_player):
        if self.state.is_terminal() or depth == 0:
            return self.state.evaluate()
        
        if maximizing_player:
            value = float('-inf')
            for action in self.state.get_possible_actions():
                value = max(value, self.minimax(depth - 1, False))
            return value
        else:
            value = float('inf')
            for action in self.state.get_possible_actions():
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
    
    def choose_action(self):
        options = ['1', '3']
        while True:
            print("Player {} choose an action:".format(self.state.current_player))
            print("1. Move a piece")
            # check if there are opponent captured pieces to recover
            if self.state.capturedPieces:
                if self.state.current_player == 'R':
                    if any(piece.startswith('B') for piece in self.state.capturedPieces):
                        print("2. Recover a captured piece")
                        options.append('2')
                else:
                    if any(piece.startswith('R') for piece in self.state.capturedPieces):
                        print("2. Recover a captured piece")
                        options.append('2')
            print("3. Exit game")
            action = input("Enter your choice: ")
            if action in options:
                return action
            else:
                print("Invalid choice, please try again.")


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
        while not self.state.is_terminal():
            self.print_board()
            action = self.choose_action()
            # TODO: only one action_apply()
            # a move basically 
            if action == '1':  # Move a piece
                move = self.get_player_move()
                self.state.make_move(move)
            elif action == '2':  # Recover a captured piece
                recovery = self.get_recovery() # recover = piece_type, (row, col)
                self.state.recover_piece(recovery)
            elif action == '3':  # Exit game
                print("Exiting the game.")
                exit()
            self.state.current_player = 'B' if self.state.current_player == 'R' else 'R'  # Switch turns
        winner = 'R' if self.state.current_player == 'B' else 'B' # should it be a class attribute?
        print("Game over! Player {} wins!".format(winner))
                

# Create a game instance and print the initial board
if __name__ == "__main__":
    game = ZeroPointOneGame()
    game.main_menu()
