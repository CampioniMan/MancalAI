from Game.GameLogicClasses import Game
from Game.Player import Player
import random


class RandomBot(Player):
	def get_title(self):
		return f"Random Player"

	def play(self, board):
		moves = Game.get_possible_moves(board, self.player_id)
		return random.choice(moves)
