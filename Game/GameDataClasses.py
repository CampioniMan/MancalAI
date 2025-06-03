from Game.MancalaUtils import CyclicList


class HoleData:
	def __init__(self, initial_stone_amount, is_mancala, player_id):
		self.stone_amount = initial_stone_amount
		self.is_mancala = is_mancala
		self.owner_id = player_id


class PlayerTerritoryData:
	def __init__(self, initial_stone_amount_per_hole, player_side_length, player_id):
		self.player_side = [HoleData(initial_stone_amount_per_hole, False, player_id) for _ in range(player_side_length)]
		self.player_mancala = HoleData(0, True, player_id)

	def get_side_stone_count(self):
		total_sum = 0
		for hole in self.player_side:
			total_sum += hole.stone_amount
		return total_sum

	def get_total_stone_count(self):
		return self.get_side_stone_count() + self.player_mancala.stone_amount


class BoardData:
	def __init__(self, player_side_length, initial_stone_amount_per_hole):
		self.player_territories = [PlayerTerritoryData(initial_stone_amount_per_hole, player_side_length, 0),
									PlayerTerritoryData(initial_stone_amount_per_hole, player_side_length, 1)]

		self.all_holes = CyclicList([])
		for player_territory in self.player_territories:
			self.all_holes.extend(player_territory.player_side)
			self.all_holes.append(player_territory.player_mancala)

	def has_ended(self):
		for player_territory in self.player_territories:
			if player_territory.get_side_stone_count() == 0:
				return True
		return False
