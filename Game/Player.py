class Player:
	def play(self, board):
		pass


class User(Player):
	def play(self, board):
		play_number = int(input())
		return play_number
