class AI:
    def __init__(self, player_color):
        self.player_color = player_color

    def choose_action(self, game_state):
        return self.minimax_move(game_state)

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
