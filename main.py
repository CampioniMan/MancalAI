from Game.GameLogicClasses import Game
from Game.Player import User
from AIBots.MinMaxBot import MinMaxBot


if __name__ == '__main__':
    player_01 = User()
    player_02 = MinMaxBot(1)
    game = Game(player_01, player_02)
    while not game.board.has_ended():
        game.draw_board()
        game.play_round()
