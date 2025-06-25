from Game.GameLogicClasses import Game
from Game.GameDataClasses import BoardData
from Game.Player import User
from AIBots.MinMaxBot import MinMaxBot
from AIBots.MancalaFocusedMinMaxBot import MancalaFocusedMinMaxBot
from AIBots.RandomBot import RandomBot
from AIBots.SmallNeuralNetworkBot import SmallNeuralNetworkBot
from AIBots.BigNeuralNetworkBot import BigNeuralNetworkBot
from AIBots.BaseNeuralNetworkBot import RangedClampNormalization
from AIBots.CompoundNeuralNetworkBot import CompoundNeuralNetworkBot


if __name__ == '__main__':
    player_side_length = 6
    initial_stone_amount_per_hole = 4
    p1_win = 0
    p2_win = 0
    tie = 0

    players = [
        #BigNeuralNetworkBot("Data/Models/BigNeuralNetworkBot/l0.800898_a0.653009_e48.keras"),
        #BigNeuralNetworkBot("Data/Models/BigNeuralNetworkBot/l0.562656_a0.782029_e22.keras"),
        CompoundNeuralNetworkBot([
            "Data/Models/BigNeuralNetworkBot/l0.794896_a0.652895_e31.keras",
            "Data/Models/BigNeuralNetworkBot/l0.800898_a0.653009_e48.keras",
            "Data/Models/BigNeuralNetworkBot/l0.802527_a0.650862_e34.keras",
            "Data/Models/BigNeuralNetworkBot/l0.806418_a0.650768_e34.keras",
            "Data/Models/BigNeuralNetworkBot/l0.808582_a0.649486_e32.keras",
            "Data/Models/BigNeuralNetworkBot/l0.815624_a0.642824_e38.keras",
            "Data/Models/BigNeuralNetworkBot/l0.821057_a0.640509_e29.keras",
        ], 0.8),
        CompoundNeuralNetworkBot([
            "Data/Models/BigNeuralNetworkBot/l0.516382_a0.783146_e43.keras",
            "Data/Models/BigNeuralNetworkBot/l0.562118_a0.765008_e15.keras",
            "Data/Models/BigNeuralNetworkBot/l0.562656_a0.782029_e22.keras",
            "Data/Models/BigNeuralNetworkBot/l0.612638_a0.747109_e18.keras",
        ], 0.5),
        #MinMaxBot(2),
    ]
    for i in range(0, len(players)):
        players[i].player_id = i

    for i in range(100):
        print(f"Welcome to MancalAI, this match will be '{players[0].get_title()}' vs '{players[1].get_title()}'")
        board = BoardData(player_side_length, initial_stone_amount_per_hole)
        game = Game(board)
        while not game.board.has_ended():
            #print()
            #game.draw_board()

            play = players[game.current_player_id].play(game.board)
            while not Game.is_valid(game.board, game.current_player_id, play):
                print(f"Try again, the play '{play}' isn't a valid option.")
                play = players[game.current_player_id].play(game.board)
            play = int(play)

            #print(f"Player '{players[game.current_player_id].get_title()}' (id={game.current_player_id:02d}) plays: {play}")
            game.play_round(play)
        #print(f"Round {i} done")
        game.draw_board()
        game.print_winner()
        player_01_score = board.player_territories[0].get_total_stone_count()
        player_02_score = board.player_territories[1].get_total_stone_count()
        if player_01_score > player_02_score:
            p1_win += 1
        elif player_02_score > player_01_score:
            p2_win += 1
        else:
            tie += 1
    print(f"p1 won {p1_win}, p2 won {p2_win} and {tie} ties happened")
