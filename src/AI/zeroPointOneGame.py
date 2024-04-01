from gameState import GameState
from ai import AI

class ZeroPointOneGame:
    def __init__(self, game_mode, depth1 = 0, depth2 = 0):
        self.game_mode = game_mode
        self.depth1 = depth1
        self.depth2 = depth2
        self.turns_count = 0
        if game_mode == 'HvAI':
            self.ai_player = AI('B')
        elif game_mode == 'AIvAI':
            self.ai_player = AI('B')
            self.ai_player_2nd = AI('R')

        self.state = GameState(
            board=[[' -- ' for _ in range(8)] for _ in range(8)],
            current_player='R',
            capturedPieces= ['B2-2', 'R1-2', 'B1-1']
        )


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
            options = []
            if self.state.current_player == 'R':
                print("Choose a black piece to recover:")
                for i, piece in enumerate(self.state.capturedPieces):
                    if piece.startswith('B'):
                        options.append(i)
                        print(f"{i}. {piece}")
            else:
                print("Choose a red piece to recover:")
                for i, piece in enumerate(self.state.capturedPieces):
                    if piece.startswith('R'):
                        options.append(i)
                        print(f"{i}. {piece}")
                        
            choice = input("Enter your choice: ")
            
            if choice.isdigit():
                if int(choice) in options:
                    return self.state.capturedPieces[int(choice)]
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

    def game_loop(self):
        while not self.state.is_terminal():
            self.print_board()
            print("The current score is: ", self.state.evaluate())
            if self.game_mode == 'HvH':
                action = self.choose_action()
                if action == '1':  # Move a piece
                    move = self.get_player_move()
                    self.state.make_move(move)
                    print("This action changed the score to: ", -self.state.evaluate())
                elif action == '2':  # Recover a captured piece
                    recovery = self.get_recovery() # recover = piece_type, (row, col)
                    self.state.recover_piece(recovery)
                    print("This action changed the score to: ", -self.state.evaluate())
                elif action == '3':  # Back to main menu
                    return
            elif self.game_mode == 'HvAI':
                if self.state.current_player == 'R':
                    action = self.choose_action()
                    if action == '1':  # Move a piece
                        move = self.get_player_move()
                        self.state.make_move(move)
                        print("This action changed the score to: ", -self.state.evaluate())
                    elif action == '2':  # Recover a captured piece
                        recovery = self.get_recovery() # recover = piece_type, (row, col)
                        self.state.recover_piece(recovery)
                        print("This action changed the score to: ", -self.state.evaluate())
                    elif action == '3':  # Back to main menu
                        return
                else:
                    action = self.ai_player.iterative_deepening_minimax(self.state, self.depth2) 
                    self.state.apply_action(action)
                    print("AI action changed the score to: ", -self.state.evaluate())
            elif self.game_mode == 'AIvAI':
                if self.state.current_player == 'B':
                    action = self.ai_player.iterative_deepening_minimax(self.state, self.depth2)
                    self.state.apply_action(action)
                    print("AI_B action changed the score to: ", -self.state.evaluate())
                else:
                    action = self.ai_player_2nd.iterative_deepening_minimax(self.state, self.depth1)
                    self.state.apply_action(action)
                    print("AI_R action changed the score to: ", -self.state.evaluate())

            self.turns_count += 1
        winner = 'R' if self.state.current_player == 'B' else 'B' 
        print("Game over! Player {} wins!".format(winner))
        print("Total turns: ", self.turns_count)
                
# with depth =2, the AIvsAI took 61 turns
