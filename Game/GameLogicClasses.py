from Game.GameDataClasses import BoardData


class Game:
	def __init__(self):
		self.player_count = 2
		self.player_side_length = 6
		self.initial_stone_amount_per_hole = 4
		self.board = BoardData(self.player_side_length, self.initial_stone_amount_per_hole)

	def loop(self):
		current_player_id = 0
		while not self.board.has_ended():
			self.draw_board()
			play = int(input())  # 1
			if not self.is_valid(play):
				print("Errou parça")
				continue

			# Traduzir o número pra qual buraco vamos usar
			selected_hole = self.board.player_territories[current_player_id].player_side[play - 1]
			# Zerar pedrinhas do primeiro
			stone_amount = self.remove_stones_from_hole(selected_hole)
			# Ir passando 1 por 1 (pular o mancala oponente) adicionando essa quantidade que tinha
			next_hole = self.get_next_hole(selected_hole)
			last_hole = self.pass_stones_around(stone_amount, next_hole)
			# Se parar no seu mancala, joga de novo
			if last_hole.is_mancala:
				continue
			# Se parar num vazio, pega o atual e o espelhado do outro lado e soma no mancala
			if last_hole.stone_amount == 1:
				self.steal_from_opponent(last_hole, current_player_id)

			current_player_id += 1
			if current_player_id >= self.player_count:
				current_player_id = 0

	def is_valid(self, play_number):
		return

	def remove_stones_from_hole(self, selected_hole):
		stones_removed = selected_hole.stone_amount
		selected_hole.stone_amount = 0
		return stones_removed

	def get_next_hole(self, selected_hole):
		return

	def pass_stones_around(self, stone_amount, next_hole):
		last_hole = next_hole
		while stone_amount > 0:
			next_hole.stone_amount += 1
			stone_amount -= 1
			last_hole = next_hole
			next_hole = self.get_next_hole(next_hole)
		return last_hole

	def steal_from_opponent(self, last_hole, current_player_id):
		return

	def draw_board(self):
		top_row_str = [f"{hole.stone_amount:02d}" for hole in self.board.player_territories[1].player_side]
		bottom_row_str = [f"{hole.stone_amount:02d}" for hole in self.board.player_territories[0].player_side]
		left_pit_str = f"{self.board.player_territories[1].player_mancala.stone_amount:02d}"
		right_pit_str = f"{self.board.player_territories[0].player_mancala.stone_amount:02d}"

		print("|    --- " + " --- ".join(top_row_str) + " ---    |")
		print(f"| {left_pit_str}{' ' * 47}{right_pit_str} |")
		print("|    --- " + " --- ".join(bottom_row_str) + " ---    |")
		return

