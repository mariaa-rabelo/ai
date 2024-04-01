class GameState:
    """
    A class to represent the state of a game.

    This class encapsulates the game board, the current player, and the pieces that have been captured.
    It provides methods to set up the board, make moves, recover captured pieces, and evaluate the game state.

    Attributes:
        board (list): A 2D list representing the game board where each element is a piece.
        current_player (str): A string indicating the current player ('R' for Red, 'B' for Blue).
        capturedPieces (list): A list of pieces that have been captured during the game.
    """

    def __init__(self, board, current_player, capturedPieces):
        """
        Constructs all the necessary attributes for the game state object.

        Args:
            board (list): A 2D list representing the initial state of the game board.
            current_player (str): The player who has the current turn.
            capturedPieces (list): The list of captured pieces at the start of the game.
        """
        self.board = board
        self.current_player = current_player
        self.capturedPieces = capturedPieces
        self.setup_pieces()

    def setup_pieces(self):
        """
        Set up the initial pieces on the board.
        """

        # Blue pieces on the first two rows
        self.board[0] = ['B0-2', 'B0-2', 'B1-1', 'B0-1', 'B1-2', 'B1-1', 'B0-2', 'B0-2']
        self.board[1] = ['B2-2'] * 8
        
        # Red pieces on the last two rows
        self.board[6] = ['R2-2'] * 8
        self.board[7] = ['R0-2', 'R0-2', 'R1-1', 'R1-2', 'R0-1', 'R1-1', 'R0-2', 'R0-2']

    def is_valid_destination(self, start_row, start_col, end_row, end_col, piece):
        """
        Check if the destination is valid for a piece to move to.

        Args:
            start_row (int): The starting row of the piece.
            start_col (int): The starting column of the piece.
            end_row (int): The destination row for the piece to move to.
            end_col (int): The destination column for the piece to move to.
            piece (str): The piece that is being moved.

        Returns:
            bool: True if the destination is valid, False otherwise.
        """

        # Check if the destination is within board limits 
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            print("Destination is out of bounds.")
            return False
        
        # Define validation rules for piece movements. The keys are piece types,
        # and the values are lambda functions that return True if the move is valid for that piece type.
        validations = {
            '2-2': lambda sr, sc, er, ec: abs(er - sr) == 2 and abs(ec - sc) == 2,
            '0-2': lambda sr, sc, er, ec: (abs(er - sr) == 2 and sc == ec) or (sr == er and abs(ec - sc) == 2),
            '1-1': lambda sr, sc, er, ec: abs(er - sr) == 1 and abs(ec - sc) == 1,
            '1-2': lambda sr, sc, er, ec: (abs(er - sr) == 1 and abs(ec - sc) == 2) or (abs(er - sr) == 2 and abs(ec - sc) == 1),
            '0-1': lambda sr, sc, er, ec: (abs(er - sr) == 1 and sc == ec) or (sr == er and abs(ec - sc) == 1),
        }

        piece_owner = piece[0]  # The owner of the piece ('R' for Red, 'B' for Blue)
        piece_type = piece[1:]  # The type of the piece ('1-1', '0-2', etc.)

        # The content of the destination cell
        destination_piece = self.board[end_row][end_col]

        # If the piece type doesn't have an entry in the validations dictionary, it's an unrecognized piece
        if piece_type not in validations:
            return False
        
        # Use the validation rule for this piece type to check if the move is valid
        if validations[piece_type](start_row, start_col, end_row, end_col):
            # If the destination square contains a piece of the same owner, it's an invalid move
            if destination_piece[0] == piece_owner:
                return False
            # If the destination square is empty or contains an opponent's piece, it's a valid move
            else:
                return True
        return False  

    def get_valid_destinations_for_piece(self, piece_row, piece_col, piece):
        """
        Get a list of valid destinations for a specific piece.

        Args:
            piece_row (int): The row of the piece.
            piece_col (int): The column of the piece.
            piece (str): The piece that is being moved.

        Returns:
            list: A list of tuples representing valid destinations.
        """

        # Determine valid destinations based on the piece's move set
        destinations = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_destination(piece_row, piece_col, row, col, piece):
                    destinations.append((row, col))
        return destinations
    
    def get_valid_recovery_positions(self, piece): # remove piece arg
        """
        Get a list of valid positions for recovering a captured piece.

        Args:
            piece (str): The captured piece to be potentially recovered.

        Returns:
            list: A list of tuples representing valid recovery positions.
        """
        
        # Find empty positions on the board where a piece can be recovered
        recovery_positions = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == ' -- ':
                    recovery_positions.append((row, col)) # TODO: check it... is it allowing occupied positions?
        return recovery_positions

    def is_terminal(self):
        """
        Check if the game has reached a terminal state.

        Returns:
            bool: True if the game is over, False otherwise.
        """

        # Determine if a 0-1 piece has been captured
        if 'R0-1' in self.capturedPieces or 'B0-1' in self.capturedPieces:
            return True
        return False

    def evaluate(self): 
        """
        Evaluate the current game state from the perspective of the current player.

        Returns:
            int: The score representing the value of the game state for the current player.
        """

         # Calculate the score based on the current state of the board
        score = 0
        for row in self.board:
            for cell in row:
                if cell.startswith(self.current_player):
                    score += 1  # Favourable to the current player
                elif cell != ' -- ':
                    score -= 1  # Favorable to the opponent
        return score

    def make_move(self, move):
        """
        Execute a move action.

        Args:
            move (tuple): A tuple containing the starting and ending coordinates of the move.
        """
        (start_row, start_col), (end_row, end_col) = move

        # Capture the opponent's piece if it exists
        if self.board[end_row][end_col] != ' -- ':
            self.capturedPieces.append(self.board[end_row][end_col])
        
        # Move the piece to the destination
        self.board[end_row][end_col] = self.board[start_row][start_col]
        
        # Clear the starting position
        self.board[start_row][start_col] = ' -- '

        # Switch the current player
        self.switch_current_player()

    def recover_piece(self, recovery):
        """
        Recover a previously captured piece to the board.

        Args:
            recovery (tuple): A tuple containing the piece to recover and its destination position.
        """
        choosen_piece, (dest_row, dest_col) = recovery
        for piece in self.capturedPieces:
            if piece == choosen_piece:
                # remove the piece from the captured pieces list
                self.capturedPieces.remove(piece)
                break

        # Transform the piece to the current player's color
        new_piece = self.current_player + choosen_piece[1:]

        # Place the recovered piece on the board
        self.board[dest_row][dest_col] = new_piece

        # Switch the current player
        self.switch_current_player()

    def apply_action(self, action):
        """
        Apply a game action which could be either a move or a recovery.

        Args:
            action (tuple): The action to apply.
        """

        # Determine the type of action and apply it to the game state
        if action[0] == 'move':
            self.make_move(action[1:])
        elif action[0] == 'recover':
            self.recover_piece(action[1:])
    
    def switch_current_player(self):
        """
        Switch the turn to the other player.
        """

        # Toggle between 'R' and 'B' to switch the current player
        self.current_player = 'B' if self.current_player == 'R' else 'R'

