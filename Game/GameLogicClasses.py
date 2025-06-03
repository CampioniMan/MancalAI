class Game:
	PLAYER_COUNT = 2

	def __init__(self, board, current_player_id=0):
		self.current_player_id = current_player_id
		self.board = board

	### Retorna True quando o usuário atual continua jogando depois dessa rodada, False caso contrário
	def play_round(self, play):
		# Traduzir o número pra qual buraco vamos usar
		selected_hole = self.board.player_territories[self.current_player_id].player_side[play - 1]
		# Zerar pedrinhas do primeiro
		stone_amount = self.remove_stones_from_hole(selected_hole)
		# Ir passando 1 por 1 (pular o mancala oponente) adicionando essa quantidade que tinha
		next_hole = self.get_next_hole(selected_hole)
		last_hole = self.pass_stones_around(stone_amount, next_hole)
		# Se parar no seu mancala, joga de novo
		if last_hole.is_mancala:
			return True
		# Se parar num vazio, pega o atual e o espelhado do outro lado e soma no mancala
		if last_hole.stone_amount == 1:
			self.steal_from_opponent(last_hole, self.current_player_id)

		self.current_player_id = Game.get_next_player_id(self.current_player_id)
		return False

	@staticmethod
	def get_next_player_id(player_id):
		return (player_id + 1) % Game.PLAYER_COUNT

	@staticmethod
	def get_possible_moves(board, player_id):
		moves = []
		for i in range(0, len(board.player_territories[player_id].player_side)):
			hole = board.player_territories[player_id].player_side[i]
			if hole.stone_amount > 0:
				moves.append(i)
		return moves

	@staticmethod
	def is_valid(board, player_id, play_number):
		if play_number is None or (isinstance(play_number, str) and not play_number.isdigit()):
			return False
		play_number = int(play_number)
		if play_number < 1 or play_number > len(board.player_territories[player_id].player_side):
			return False
		return board.player_territories[player_id].player_side[play_number - 1].stone_amount > 0

	def remove_stones_from_hole(self, selected_hole):
		stones_removed = selected_hole.stone_amount
		selected_hole.stone_amount = 0
		return stones_removed

	def get_next_hole(self, selected_hole):
		current_index = self.board.all_holes.index(selected_hole)
		return self.board.all_holes[current_index + 1]

	def pass_stones_around(self, stone_amount, next_hole):
		last_hole = next_hole
		while stone_amount > 0:
			if next_hole.is_mancala and next_hole.owner_id != self.current_player_id:
				next_hole = self.get_next_hole(next_hole)
				continue
			next_hole.stone_amount += 1
			stone_amount -= 1
			last_hole = next_hole
			next_hole = self.get_next_hole(next_hole)
		return last_hole

	def steal_from_opponent(self, last_hole, current_player_id):
		last_hole_index = self.board.all_holes.index(last_hole)
		opposite_index = 2 * self.board.player_side_length - last_hole_index
		opposite_hole = self.board.all_holes[opposite_index]
		
		if opposite_hole.owner_id == current_player_id or opposite_hole.stone_amount == 0:
			return
		
		total_stones = last_hole.stone_amount + opposite_hole.stone_amount
		last_hole.stone_amount = 0
		opposite_hole.stone_amount = 0
		
		self.board.player_territories[current_player_id].player_mancala.stone_amount += total_stones

	def draw_board(self):
		top_row_str = [f"{hole.stone_amount:02d}" for hole in self.board.player_territories[1].player_side[::-1]]
		bottom_row_str = [f"{hole.stone_amount:02d}" for hole in self.board.player_territories[0].player_side]
		left_pit_str = f"{self.board.player_territories[1].player_mancala.stone_amount:02d}"
		right_pit_str = f"{self.board.player_territories[0].player_mancala.stone_amount:02d}"

		print("|    --- " + " --- ".join(top_row_str) + " ---    |")
		print(f"| {left_pit_str}{' ' * 47}{right_pit_str} |")
		print("|    --- " + " --- ".join(bottom_row_str) + " ---    |")
		return

	def print_winner(self):
		player_01_score = self.board.player_territories[0].player_mancala.stone_amount
		player_02_score = self.board.player_territories[1].player_mancala.stone_amount
		print(f"Game Over!")
		print(f"Player 1 Score: {player_01_score}")
		print(f"Player 2 Score: {player_02_score}")
		if player_01_score > player_02_score:
			print("Player 1 wins!")
		elif player_02_score > player_01_score:
			print("Player 2 wins!")
		else:
			print("It's a tie!")
