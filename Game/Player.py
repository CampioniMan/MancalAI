class Player:
	def play(self, board):
		pass


class User(Player):
	def play(self, board):
		print("User plays: ", end="")
		play_number = input()
		return play_number
