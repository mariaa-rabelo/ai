import copy
class AI:
    def __init__(self, player_color):
        self.player_color = player_color

    # def choose_action(self, game_state):
    #     return self.minimax_move(game_state)

    def minimax(self, game_state, depth, maximizing_player):
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
    
    def choose_action(self, game_state):
        # Exemplo simplificado
        # chamar um método Minimax e avaliar o resultado de várias ações possíveis.
        best_action = None
        best_score = float('-inf')

        for action in self.get_possible_actions(game_state, self.player_color):
            temp_game_state = copy.deepcopy(game_state)
            temp_game_state.apply_action(action)
            score = temp_game_state.evaluate()
            if score > best_score:
                best_score = score
                best_action = action

            # score = self.minimax(new_game_state, 3, not maximizing_player)
            # if maximizing_player and score > best_score or not maximizing_player and score < best_score:
            #     best_score = score
            #     best_action = action

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
            if captured_piece.startswith(player_color):
                recovery_positions = game_state.get_valid_recovery_positions(captured_piece) 
                for recovery_pos in recovery_positions:
                    possible_actions.append(('recover', captured_piece, recovery_pos))

        return possible_actions
