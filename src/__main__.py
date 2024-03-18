from gameState import GameState
from ai import AI

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
        destinations= self.state.get_valid_recovery_positions(piece)
        
        dest_row, dest_col = self.get_destination(destinations)
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
            print("3. Back to main menu")
            action = input("Enter your choice: ")
            if action in options:
                return action
            else:
                print("Invalid choice, please try again.")


    def main_menu(self):
        while True:
            print("Welcome to Zero Point One! :)")
            print("1. Human vs. Human")
            print("2. Human vs. AI")
            print("3. AI vs. AI")
            print("4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.game_mode = 'HvH'
                self.game_loop()
            elif choice == '2':
                self.ai_player = AI('B') 
                self.game_mode = 'HvAI'
                self.game_loop()
            elif choice == '3':
                self.ai_player = AI('B')
                self.game_mode = 'AIvAI'
                print("AI functionality is not yet implemented. Please choose another option.")
            elif choice == '4':
                print("Exiting the game.")
                break
            else:
                print("Invalid choice, please try again.")

    # TODO: only one action_apply()
    # a move basically 
    def game_loop(self):
        while not self.state.is_terminal():
            self.print_board()
            if self.game_mode == 'HvH':
                action = self.choose_action()
                if action == '1':  # Move a piece
                    move = self.get_player_move()
                    self.state.make_move(move)
                elif action == '2':  # Recover a captured piece
                    recovery = self.get_recovery() # recover = piece_type, (row, col)
                    self.state.recover_piece(recovery)
                elif action == '3':  # Back to main menu
                    return
            elif self.game_mode == 'HvAI':
                if self.state.current_player == 'R':
                    action = self.choose_action()
                    if action == '1':  # Move a piece
                        move = self.get_player_move()
                        self.state.make_move(move)
                    elif action == '2':  # Recover a captured piece
                        recovery = self.get_recovery() # recover = piece_type, (row, col)
                        self.state.recover_piece(recovery)
                    elif action == '3':  # Back to main menu
                        return
                else:
                    action = self.ai_player.choose_action(self.state)
                    self.state.apply_action(action)
            self.state.current_player = 'B' if self.state.current_player == 'R' else 'R'  # Switch turns
        winner = 'R' if self.state.current_player == 'B' else 'B' # should it be a class attribute?
        print("Game over! Player {} wins!".format(winner))
                

# Create a game instance and print the initial board
if __name__ == "__main__":
    game = ZeroPointOneGame()
    game.main_menu()
