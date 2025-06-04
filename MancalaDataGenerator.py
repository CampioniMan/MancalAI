#  Esse código gera arquivos de estado de jogo e o que seria a melhor jogada a ser feita, de acordo com o bot minmax
from Game.GameLogicClasses import Game
from Game.GameDataClasses import BoardData
from Game.Player import User
from AIBots.MinMaxBot import MinMaxBot
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


parser = argparse.ArgumentParser("Mancala Data Generator")
parser.add_argument("count", help="How many games will be played in this configuration. It is also the number of files generated.", type=int)
parser.add_argument("--bot_1_depth", "-b1", help="Depth of the first MinMaxBot (default is 6).", type=int, required=False, default=6)
parser.add_argument("--bot_2_depth", "-b2", help="Depth of the second MinMaxBot (default is 6).", type=int, required=False, default=6)
args = parser.parse_args()

for i in range(args.count):
    gathered_data = []

    player_side_length = 6
    initial_stone_amount_per_hole = 4

    players = [MinMaxBot(args.bot_1_depth), MinMaxBot(args.bot_2_depth)]
    for i in range(0, len(players)):
        players[i].player_id = i
    print(f"Generating training data from bots: '{players[0].get_title()}' and '{players[1].get_title()}'")

    board = BoardData(player_side_length, initial_stone_amount_per_hole)
    game = Game(board)
    while not game.board.has_ended():
        play = players[game.current_player_id].play(game.board)
        while not Game.is_valid(game.board, game.current_player_id, play):
            print("Errou parça, tenta de novo")
            play = players[game.current_player_id].play(game.board)
        play = int(play)
        gathered_data.append((get_board_state_vector(game.board), game.current_player_id, play))

        game.play_round(play)
    game.draw_board()
    game.print_winner()

    crc = get_data_crc32(gathered_data)

    filename = f"Data/{crc}.json"

    if os.path.exists(filename):
        print("This game was already generated before")
        exit(0)

    with open(filename, 'w') as f:
        for state_vector, player_id, move in gathered_data:
            record = {"sv": state_vector, "p": player_id, "m": move}
            f.write(json.dumps(record) + '\n')
    print(f"Data point {i+1} saved to {filename}")
