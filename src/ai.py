import copy
class AI:
    def __init__(self, player_color):
        self.player_color = player_color

    def minimax(self, game_state, depth, alpha, beta, maximizing_player):
        
        if game_state.is_terminal() or depth == 0:
            # print(f"at depth {depth}. Score: {game_state.evaluate()}")
            if (maximizing_player):
                return game_state.evaluate(), None
            return -game_state.evaluate(), None # invert score 
        
        if maximizing_player:
            max_score = float('-inf')
            best_action = None
            for action in self.get_possible_actions(game_state, game_state.current_player):
                new_game_state = copy.deepcopy(game_state)
                new_game_state.apply_action(action)
                score, _  = self.minimax(new_game_state, depth - 1, alpha, beta, False)
                if score > max_score:
                    max_score = score
                    best_action = action
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            # print(f"Max score: {max_score}, Best action: {best_action} for player {game_state.current_player} with depth {depth}")
            return max_score, best_action
        else:
            min_score = float('inf')
            best_action = None
            for action in self.get_possible_actions(game_state, game_state.current_player):
                new_game_state = copy.deepcopy(game_state)
                new_game_state.apply_action(action)
                score, _ = self.minimax(new_game_state, depth - 1, alpha, beta, True)
                if score < min_score:
                    # print(f"score {score} < min_score {min_score}, action {action} better than best_action {best_action} for player {game_state.current_player} with depth {depth}")
                    min_score = score
                    best_action = action
                beta = min(beta, score)
                if beta <= alpha:
                    break
            # print()
            # print(f"Min score: {min_score}, Best action: {best_action} for player {game_state.current_player} with depth {depth}")
            return min_score, best_action
       

    def iterative_deepening_minimax(self, game_state, max_depth):
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
        possible_actions = []

        # Gerar ações de movimento
        for row in range(8):
            for col in range(8):
                piece = game_state.board[row][col]
                # Verifique se a peça pertence ao jogador atual
                if piece.startswith(player_color):
                    destinations = game_state.get_valid_destinations_for_piece(row, col, piece)
                    for dest in destinations:
                        possible_actions.append(('move', (row, col), dest))

        # Gerar ações de recuperação se houver peças capturadas disponíveis
        for captured_piece in game_state.capturedPieces:
            if not captured_piece.startswith(player_color):
                recovery_positions = game_state.get_valid_recovery_positions(captured_piece) 
                for recovery_pos in recovery_positions:
                    possible_actions.append(('recover', captured_piece, recovery_pos))

        return possible_actions
