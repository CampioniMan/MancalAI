from Game.GameLogicClasses import Game
from Game.GameDataClasses import BoardData
from Game.Player import User
from AIBots.MinMaxBot import MinMaxBot


if __name__ == '__main__':
    player_side_length = 6
    initial_stone_amount_per_hole = 4

    players = [User(), MinMaxBot(1)]
    board = BoardData(player_side_length, initial_stone_amount_per_hole)
    game = Game(board)
    while not game.board.has_ended():
        game.draw_board()

        play = players[game.current_player_id].play(game.board)
        while not Game.is_valid(game.board, game.current_player_id, play):
            print("Errou parça, tenta de novo")
            play = players[game.current_player_id].play(game.board)
        play = int(play)

        game.play_round(play)
    game.draw_board()
    game.print_winner()
