class Player:
	player_id = -1

	def play(self, board):
		pass

	def get_title(self):
		pass


class User(Player):
	def play(self, board):
		print("User plays: ", end="")
		play_number = input()
		return play_number

	def get_title(self):
		return "User"
