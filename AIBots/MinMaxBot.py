from Game.GameLogicClasses import Game
from Game.GameDataClasses import BoardData


class MinMaxBot:
    def __init__(self, bot_player_id):
        self.max_depth = 8
        self.maximizing_player_id = bot_player_id

    def get_next_action(self, board):
        return self.minimax(board, 0, True)

    def minimax(self, board, current_depth, current_player_id):
        if board.has_ended() or current_depth == self.max_depth:
            return board.player_territories[self.maximizing_player_id].get_total_stone_count()

        if current_player_id == self.maximizing_player_id:
            best_score = -float('inf')
            for move in board.get_possible_moves(self.maximizing_player_id):
                new_board = self.make_move(board, move)
                score = self.minimax(new_board, current_depth + 1, Game.get_next_player_id(current_player_id))
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in board.get_possible_moves(current_player_id):
                new_board = self.make_move(board, move)
                score = self.minimax(new_board, current_depth + 1, Game.get_next_player_id(current_player_id))
                best_score = min(best_score, score)
            return best_score

    def make_move(self, board, move):
        #TODO: Make the move
        return board
