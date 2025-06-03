from Game.GameLogicClasses import Game
from Game.Player import Player
import copy


class MinMaxBot(Player):
    def __init__(self):
        self.max_depth = 5

    def play(self, board):
        (play, score) = self.minimax(board, 0, self.player_id)
        print(f"MinMaxBot plays: {play}")
        return play

    def minimax(self, board, current_depth, current_player_id):
        if board.has_ended() or current_depth == self.max_depth:
            return None, board.player_territories[self.player_id].get_total_stone_count()

        if current_player_id == self.player_id:
            best_play = None
            best_score = -float('inf')
            for move in Game.get_possible_moves(board, current_player_id):
                (new_board, next_player) = self.make_move(board, current_player_id, move)
                (play, score) = self.minimax(new_board, current_depth + 1, next_player)
                if score > best_score:
                    best_play = move
                    best_score = score
            return best_play, best_score
        else:
            best_play = None
            best_score = float('inf')
            for move in Game.get_possible_moves(board, current_player_id):
                (new_board, next_player) = self.make_move(board, current_player_id, move)
                (play, score) = self.minimax(new_board, current_depth + 1, next_player)
                if score < best_score:
                    best_play = move
                    best_score = score
            return best_play, best_score

    def make_move(self, board, player_id, move):
        board_with_move = copy.deepcopy(board)
        game = Game(board_with_move, player_id)
        game.play_round(move)
        return game.board, game.current_player_id
