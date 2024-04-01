from gameState import GameState
from ai import AI

class ZeroPointOneGame:
    """
    Class to manage the game logic for Zero Point One.

    This class manages the game loop, interactions with players, and uses the AI for making moves
    in different game modes: Human vs. Human, Human vs. AI, and AI vs. AI.

    Attributes:
        game_mode (str): The mode of the game which determines the type of players (Human or AI).
        turns_count (int): Counter for the number of turns taken in the game.
        ai_player (AI): The AI player instance for one of the players if applicable.
        ai_player_2nd (AI): The second AI player instance for AI vs. AI mode if applicable.
        state (GameState): The current state of the game, holding the board, players, and captured pieces.
    """

    def __init__(self, game_mode, depth1 = 0, depth2 = 0):
        """
        Initialize the game with the specified mode and setup the initial game state.

        Args:
            game_mode (str): The mode of the game ('HvH', 'HvAI', or 'AIvAI').
            depth1 (int): Max depth to use in iterative deepening minimax for Red, if applicable
            depth2 (int): Max depth to use in iterative deepening minimax for Blue, if applicable
        """
        self.game_mode = game_mode
        self.depth1 = depth1
        self.depth2 = depth2
        self.turns_count = 0

        # Initialize AI players depending on the game mode
        if game_mode == 'HvAI':
            self.ai_player = AI('B') # Human vs AI, AI plays as Blue
        elif game_mode == 'AIvAI':
            self.ai_player = AI('B') # AI vs AI, first AI plays as Blue
            self.ai_player_2nd = AI('R') # Second AI plays as Red

        # Initialize the game state with an empty board, set the current player, and an empty list of captured pieces
        self.state = GameState(
            board=[[' -- ' for _ in range(8)] for _ in range(8)],
            current_player='R',
            capturedPieces= []
        )

    def print_board(self):
        """
        Print the game board in a human-readable format, along with the captured pieces.
        """

        # Display the column numbers
        print('    ' + '    '.join(str(col) for col in range(8)))

        # Display the board row by row
        for row_num, row in enumerate(self.state.board):
            print(str(row_num) + ' ' + ' '.join(row))
        print()

        # Display the captured pieces
        print("Captured pieces: ", self.state.capturedPieces)
    
    def get_player_piece(self):
        """
        Prompt the human player to select a piece to move.

        This function ensures the player chooses a piece that belongs to them. It handles input and validates the selection.

        Returns:
            tuple: The coordinates of the selected piece as (row, col).
        """

       # Input handling logic for selecting a piece
        while True:
            try:
                piece_input = input(f"Player {self.state.current_player}, enter the coordinates of the piece to move (row, col): ")
                row, col = map(int, piece_input.split(','))
                # Check if the piece belongs to the current player
                if self.state.board[row][col].startswith(self.state.current_player):
                    return (row, col)
                else:
                    print("That is not your piece. Please choose one of your own pieces.")
            except (ValueError, IndexError):
                # Handle incorrect input formats
                print("Invalid input. Please enter coordinates in the format 'row, col'.")

    def get_destination(self, destinations):
        """
        Prompt the player for a destination to move their selected piece to.

        The function lists valid destinations and ensures the player selects from these options.

        Args:
            destinations (list): A list of valid destination coordinates.

        Returns:
            tuple: The chosen destination coordinates as (row, col).
        """

        # Input handling logic for selecting a destination
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
        """
        Manage the process of a human player making a move.

        This involves selecting a piece and then a valid destination for that piece.

        Returns:
            tuple: A move represented by start and end coordinates ((start_row, start_col), (end_row, end_col)).
        """

        # Get the coordinates of the piece to move
        piece_row, piece_col = self.get_player_piece()

        # Get the piece at the selected coordinates
        piece = self.state.board[piece_row][piece_col]

        # Get the valid destinations for the selected piece
        destinations = self.state.get_valid_destinations_for_piece(piece_row, piece_col, piece)
        
        # Handle the case where there are no valid moves for the selected piece
        while not destinations:
            print("No valid moves for this piece. Please choose another piece.")
            piece_row, piece_col = self.get_player_piece()
            piece = self.state.board[piece_row][piece_col]
            destinations = self.state.get_valid_destinations_for_piece(piece_row, piece_col, piece)

        # Display the possible destinations for the selected piece
        print(f"Possible destinations for {piece} at ({piece_row}, {piece_col}):")
        for dest in destinations:
            print(dest)
        
        # Get the destination coordinates from the player
        dest_row, dest_col = self.get_destination(destinations)

        # Return the move as a tuple of start and end coordinates
        return (piece_row, piece_col), (dest_row, dest_col)
    

    def get_recovery(self): 
        """
        Handle the recovery of a captured piece by the player.

        Returns:
            tuple: The recovery action, including the chosen piece and its destination.
        """

        # Logic for a player to recover a captured piece
        piece = self.choose_captured_piece()
        destinations= self.state.get_valid_recovery_positions(piece)
        dest_row, dest_col = self.get_destination(destinations)

        # Return the recovery action as a tuple
        return piece, (dest_row, dest_col)

    def choose_captured_piece(self):
        """
        Prompt the player to select one of their captured pieces for recovery.

        Returns:
            str: The chosen piece to be potentially recovered.
        """

        # Input handling logic for selecting a captured piece
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
        """
        Allow the player to choose an action: move a piece, recover a captured piece, or return to the main menu.

        Returns:
            str: The chosen action as '1', '2', or '3'.
        """
        options = ['1', '3']

        # Input handling logic for choosing an action
        while True:
            print("Player {} choose an action:".format(self.state.current_player))
            print("1. Move a piece")
            # check if there are captured pieces to recover
            if self.state.capturedPieces:
                # Check for opponent's pieces to recover
                if self.state.current_player == 'R':
                    if any(piece.startswith('B') for piece in self.state.capturedPieces):
                        print("2. Recover a captured piece")
                        options.append('2')
                else:
                    if any(piece.startswith('R') for piece in self.state.capturedPieces):
                        print("2. Recover a captured piece")
                        options.append('2')
            print("3. Back to main menu")

            # Get the player's choice
            action = input("Enter your choice: ")
            if action in options:
                return action
            else:
                print("Invalid choice, please try again.")

    def game_loop(self):
        """
        Run the main game loop.

        This method controls the flow of the game, alternating between players' turns and managing AI actions.
        """

        # Main game loop handling turns, actions, and game termination
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
                
