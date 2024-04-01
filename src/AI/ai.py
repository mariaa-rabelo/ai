import copy
class AI:
    """
    Artificial Intelligence for playing a game.
    
    This AI is capable of playing games where moves can be evaluated using
    iterative deepening with the minimax algorithm, with alpha-beta pruning for optimization. 
    Attributes:
        player_color (str): The designated color of the AI player, used to
                            determine its moves in the game.
    """
    def __init__(self, player_color):
        """
        Initializes the AI with the given player color.
        
        Args:
            player_color (str): The color representing the AI player.
        """
        self.player_color = player_color

    def minimax(self, game_state, depth, alpha, beta, maximizing_player):
        """
        Performs the minimax algorithm to evaluate game states and determine the
        best move for the AI player.

        This is a recursive function that considers the game state's possible
        future states and chooses the optimal move. The recursion is limited by
        the depth parameter, and the function utilizes alpha-beta pruning to
        improve performance by eliminating suboptimal branches.

        Args:
            game_state (object): The current state of the game.
            depth (int): The maximum depth of the game tree to explore.
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.
            maximizing_player (bool): True if the AI is the maximizer, False otherwise.

        Returns:
            tuple: A tuple containing the score of the best move and the move itself.
        """

        # Base case: if the game is over or the depth is zero
        if game_state.is_terminal() or depth == 0:
            if (maximizing_player):
                return game_state.evaluate(), None
            return -game_state.evaluate(), None # invert score 
        
        # Maximizing player: aims to maximize the score
        if maximizing_player:
            max_score = float('-inf')
            best_action = None
            for action in self.get_possible_actions(game_state, game_state.current_player):
                # Simulate the move
                new_game_state = copy.deepcopy(game_state)
                new_game_state.apply_action(action)
                # Recursive call
                score, _  = self.minimax(new_game_state, depth - 1, alpha, beta, False)
                if score > max_score:
                    max_score = score
                    best_action = action
                alpha = max(alpha, score)
                if beta <= alpha: # Alpha-beta pruning
                    break
            return max_score, best_action
        # Minimizing player: aims to minimize the score
        else:
            min_score = float('inf')
            best_action = None
            for action in self.get_possible_actions(game_state, game_state.current_player):
                # Simulate the move
                new_game_state = copy.deepcopy(game_state)
                new_game_state.apply_action(action)
                # Recursive call
                score, _ = self.minimax(new_game_state, depth - 1, alpha, beta, True)
                if score < min_score:
                    min_score = score
                    best_action = action
                beta = min(beta, score)
                if beta <= alpha: # Alpha-beta pruning
                    break
            return min_score, best_action
       

    def iterative_deepening_minimax(self, game_state, max_depth):
        """
        Uses iterative deepening alongside the minimax algorithm to iteratively
        deepen the search for the best move.

        This approach starts with a shallow search and progressively deepens the
        search allowing a flexible time management of move selection.

        Args:
            game_state (object): The current state of the game.
            max_depth (int): The maximum depth to which the AI should search.

        Returns:
            The best move determined by the minimax algorithm.
        """
        print(f"Player {game_state.current_player} is thinking...")
        print(f"Current score: {game_state.evaluate()}")
        print()
        best_score = float('-inf') 
        best_action = None
        for depth in range(1, max_depth + 1):
            print(f"Thinking at depth {depth}...")
            print()
            score, action = self.minimax(game_state, depth, float('-inf'), float('inf'), True)
            if score > best_score:
                best_score = score
                best_action = action
            print(f"Until depth {depth}, best score {best_score} for best action: {best_action}")
        print()
        return best_action

    def get_possible_actions(self, game_state, player_color):
        """
        Generates all possible actions for the player given the current state of the game.

        Args:
            game_state (object): The current state of the game.
            player_color (str): The color representing the player for whom to generate actions.

        Returns:
            list: A list of all possible actions the player can take.
        """
        possible_actions = []
        # Generate move actions for the player
        for row in range(8):
            for col in range(8):
                piece = game_state.board[row][col]
                if piece.startswith(player_color):
                    destinations = game_state.get_valid_destinations_for_piece(row, col, piece)
                    for dest in destinations:
                        possible_actions.append(('move', (row, col), dest))

        # Generate recovery actions if there are any captured pieces available
        for captured_piece in game_state.capturedPieces:
            if not captured_piece.startswith(player_color):
                recovery_positions = game_state.get_valid_recovery_positions(captured_piece) 
                for recovery_pos in recovery_positions:
                    possible_actions.append(('recover', captured_piece, recovery_pos))

        return possible_actions
