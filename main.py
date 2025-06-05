from Game.GameLogicClasses import Game
from Game.GameDataClasses import BoardData
from Game.Player import User
from AIBots.MinMaxBot import MinMaxBot
from AIBots.RandomBot import RandomBot


if __name__ == '__main__':
    player_side_length = 6
    initial_stone_amount_per_hole = 4

    players = [RandomBot(), MinMaxBot(6)]
    for i in range(0, len(players)):
        players[i].player_id = i
    print(f"Welcome to MancalAI, this match will be '{players[0].get_title()}' vs '{players[1].get_title()}'")
    board = BoardData(player_side_length, initial_stone_amount_per_hole)
    game = Game(board)
    while not game.board.has_ended():
        print()
        game.draw_board()

        play = players[game.current_player_id].play(game.board)
        while not Game.is_valid(game.board, game.current_player_id, play):
            print("Errou parça, tenta de novo")
            play = players[game.current_player_id].play(game.board)
        play = int(play)

        print(f"Player '{players[game.current_player_id].get_title()}' (id={game.current_player_id:02d}) plays: {play}")
        game.play_round(play)
    game.draw_board()
    game.print_winner()
