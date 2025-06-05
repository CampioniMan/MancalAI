from Game.GameLogicClasses import Game
from Game.Player import Player
from multiprocessing import Pool
import copy
import random


class MinMaxBot(Player):
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def get_title(self):
        return f"MinMaxBot (depth={self.max_depth})"

    def play(self, board):
        if self.max_depth <= 4:
            (play, score) = MinMaxBot.minmax(board, 0, self.player_id, self.player_id, self.max_depth)
            return play
        else:
            possibilities = Game.get_possible_moves(board, self.player_id)
            num_processes = min(board.player_side_length, len(possibilities))
            if num_processes == 0:
                return None

            with Pool(processes=num_processes) as pool:
                multiple_results = [pool.apply_async(MinMaxBot.minmax_threaded, (board, 1, copy.copy(self.player_id), copy.copy(self.player_id), copy.copy(self.max_depth), possibility)) for possibility in possibilities]
                results = [res.get(timeout=10) for res in multiple_results]

                best_play = None
                best_score = -float('inf')
                for play, score in results:
                    if score > best_score:
                        best_play = play
                        best_score = score

                return best_play

    @staticmethod
    def minmax_threaded(board, current_depth, current_player_id, bot_player_id, max_depth, chosen_play):
        (new_board, next_player) = MinMaxBot.make_move(board, current_player_id, chosen_play)
        (last_play, score) = MinMaxBot.minmax(new_board, current_depth, next_player, bot_player_id, max_depth)
        return chosen_play, score

    @staticmethod
    def minmax(board, current_depth, current_player_id, bot_player_id, max_depth):
        if board.has_ended() or current_depth == max_depth:
            return None, board.player_territories[bot_player_id].get_total_stone_count()

        if current_player_id == bot_player_id:
            best_play = None
            best_score = -float('inf')
            for move in Game.get_possible_moves(board, current_player_id):
                (new_board, next_player) = MinMaxBot.make_move(board, current_player_id, move)
                (play, score) = MinMaxBot.minmax(new_board, current_depth + 1, next_player, bot_player_id, max_depth)
                if score > best_score:
                    best_play = move
                    best_score = score
            return best_play, best_score
        else:
            best_play = None
            best_score = float('inf')
            for move in Game.get_possible_moves(board, current_player_id):
                (new_board, next_player) = MinMaxBot.make_move(board, current_player_id, move)
                (play, score) = MinMaxBot.minmax(new_board, current_depth + 1, next_player, bot_player_id, max_depth)
                if score < best_score:
                    best_play = move
                    best_score = score
            return best_play, best_score

    @staticmethod
    def make_move(board, player_id, move):
        board_with_move = copy.deepcopy(board)
        game = Game(board_with_move, player_id)
        game.play_round(move)
        return game.board, game.current_player_id
