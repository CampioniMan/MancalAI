from Game.GameLogicClasses import Game
from Game.GameDataClasses import BoardData
from Game.Player import User
from AIBots.MinMaxBot import MinMaxBot
from AIBots.MancalaFocusedMinMaxBot import MancalaFocusedMinMaxBot
from AIBots.RandomBot import RandomBot
from AIBots.SmallNeuralNetworkBot import SmallNeuralNetworkBot


if __name__ == '__main__':
    player_side_length = 6
    initial_stone_amount_per_hole = 4
    p1_win = 0
    p2_win = 0
    tie = 0

    players = [
        SmallNeuralNetworkBot("Data/Models/BigNeuralNetworkBot/l1.286234_a0.491005_e100.keras"),
        MancalaFocusedMinMaxBot(1),
        #MinMaxBot(6)
    ]
    for i in range(0, len(players)):
        players[i].player_id = i

    for i in range(30):
        print(f"Welcome to MancalAI, this match will be '{players[0].get_title()}' vs '{players[1].get_title()}'")
        board = BoardData(player_side_length, initial_stone_amount_per_hole)
        game = Game(board)
        while not game.board.has_ended():
            #print()
            #game.draw_board()

            play = players[game.current_player_id].play(game.board)
            while not Game.is_valid(game.board, game.current_player_id, play):
                #print(f"Try again, the play '{play}' isn't a valid option.")
                play = players[game.current_player_id].play(game.board)
            play = int(play)

            #print(f"Player '{players[game.current_player_id].get_title()}' (id={game.current_player_id:02d}) plays: {play}")
            game.play_round(play)
        print(f"Round {i} done")
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
