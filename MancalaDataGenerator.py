#  Esse código gera arquivos de estado de jogo e o que seria a melhor jogada a ser feita, de acordo com o bot minmax
from Game.GameLogicClasses import Game
from Game.GameDataClasses import BoardData
from Game.Player import User
from AIBots.MinMaxBot import MinMaxBot
from AIBots.RandomBot import RandomBot
import json
import zlib
import os
import argparse


def get_board_state_vector(board_data: BoardData) -> list[int]:
	state_vector = []
	for hole in board_data.all_holes:
		state_vector.append(hole.stone_amount)
	return state_vector


def get_data_crc32(training_data: list) -> int:
	serialized_data = json.dumps(training_data, sort_keys=True, separators=(',', ':'))
	data_bytes = serialized_data.encode('utf-8')
	crc_value = zlib.crc32(data_bytes)
	return crc_value


parser = argparse.ArgumentParser("Mancala Data Generator", allow_abbrev=False)
parser.add_argument("count",
                    help="How many games will be played in this configuration. It is also the number of files generated.",
                    type=int)

first_bot_group = parser.add_mutually_exclusive_group(required=True)
first_bot_group.add_argument("--bot_1_depth", "-b1d", help="Depth of the first MinMaxBot.", type=int)
first_bot_group.add_argument("--bot_1_random", "-b1r", help="Sets the first bot as random (no data saved).", action='store_true')

second_bot_group = parser.add_mutually_exclusive_group(required=True)
second_bot_group.add_argument("--bot_2_depth", "-b2d", help="Depth of the second MinMaxBot.", type=int)
second_bot_group.add_argument("--bot_2_random", "-b2r", help="Sets the second bot as random (no data saved).", action='store_true')

args = parser.parse_args()

player_side_length = 6
initial_stone_amount_per_hole = 4

players = []
if args.bot_1_random:
	players.append(RandomBot())
else:
	players.append(MinMaxBot(args.bot_1_depth))

if args.bot_2_random:
	players.append(RandomBot())
else:
	players.append(MinMaxBot(args.bot_2_depth))

for i in range(0, len(players)):
	players[i].player_id = i

for i in range(args.count):
	gathered_data = []
	print(f"Generating training data from bots: '{players[0].get_title()}' and '{players[1].get_title()}'")

	board = BoardData(player_side_length, initial_stone_amount_per_hole)
	game = Game(board)
	while not game.board.has_ended():
		play = players[game.current_player_id].play(game.board)
		while not Game.is_valid(game.board, game.current_player_id, play):
			print("Errou parça, tenta de novo")
			play = players[game.current_player_id].play(game.board)
		play = int(play)

		if not isinstance(players[game.current_player_id], RandomBot):
			gathered_data.append((get_board_state_vector(game.board), game.current_player_id, play))
		else:
			minmax_bot = MinMaxBot(5)
			minmax_play = int(minmax_bot.play(game.board))
			gathered_data.append((get_board_state_vector(game.board), game.current_player_id, minmax_play))

		game.play_round(play)
	print()
	game.draw_board()
	game.print_winner()

	if len(gathered_data) == 0:
		print("This game was useless. No data will be saved.")
		continue

	crc = get_data_crc32(gathered_data)

	filename = f"Data/Random_vs_Random/{crc}.json"

	if os.path.exists(filename):
		print("This game was already generated before")
		continue

	with open(filename, 'w') as f:
		for state_vector, player_id, move in gathered_data:
			record = {"sv": state_vector, "p": player_id, "m": move}
			f.write(json.dumps(record) + '\n')
	print(f"Data point {i + 1} saved to {filename}")
