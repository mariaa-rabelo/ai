import copy
class AI:
    def __init__(self, player_color):
        self.player_color = player_color

    def minimax(self, game_state, depth, maximizing_player):
        if game_state.is_terminal() or depth == 0:
            return game_state.evaluate(), None # None?
        
        best_action = None
        if maximizing_player:
            bestScore = float('-inf')
            for action in self.get_possible_actions(game_state, self.player_color):
                new_game_state = copy.deepcopy(game_state)
                new_game_state.apply_action(action)
                score, _ = self.minimax(new_game_state, depth - 1, False)
                if score > bestScore:
                    bestScore = score
                    best_action = action
        else:
            bestScore = float('inf') # if not maximizing_player, the best score is the lowest possible
            for action in self.get_possible_actions(game_state, self.player_color):
                new_game_state = copy.deepcopy(game_state)
                new_game_state.apply_action(action)
                score, _ = self.minimax(new_game_state, depth - 1, True)
                if score < bestScore:
                    bestScore = score
                    best_action = action
        return bestScore, best_action

    def iterative_deepening_minimax(self, game_state, max_depth): # deveria ser apenas uma função?
        best_score = float('-inf') 
        for depth in range(1, max_depth + 1):
            score, action = self.minimax(game_state, depth, True)
            print(f"Depth: {depth}, Score: {score}, Action: {action}")
            if score > best_score:
                best_score = score
                best_action = action
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
