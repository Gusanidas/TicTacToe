from board import Board
from players import Player


class Game:

    def __init__(self, player1: Player, player2: Player):
        self.players = (player1, player2)

    def start(self):
        board = Board()
        print("To choose a cell, enter the corresponding number:")
        board.print_board(print_positions=True)
        print("Let's begin!")
        turn, moves, victory = 0, 0, False
        while moves < 9 and not victory:
            player = self.players[turn]
            try:
                new_position = player.move(board.board)
                victory = board.move(player.symbol, new_position)
            except ValueError:
                continue
            turn = (turn + 1) % 2
            moves += 1
            board.print_board()
            print(" ")
        if victory:
            turn = (turn + 1) % 2
            print("Victory!! Player {} has won in {} moves".format(
                self.players[turn].symbol, moves))
        else:
            print("The game ended in a tie.")
        