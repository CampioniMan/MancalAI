from GameDataClasses import BoardData


class Game:
	def __init__(self):
		self.player_side_length = 6
		self.initial_stone_amount_per_hole = 4
		self.board = BoardData(self.player_side_length, self.initial_stone_amount_per_hole)
