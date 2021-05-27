# Class representing the tic tac toe board. With methods to display the
# board and to check if a move has resulted in victory.

class Board:

    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.winning_combinations = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6))

    def move(self, player_symbol: str, position: int) -> bool:
        if position < 0 or position > 8 or self.board[position] != " ":
            raise ValueError
        self.board[position] = player_symbol
        return self._check_victory(player_symbol)

    def print_board(self, print_positions: bool = False) -> None:
        print("*************")
        for row in range(3):
            if print_positions:
                print("* {} | {} | {} *".format(3 * row + 1, 3 * row + 2,
                                                3 * row + 3))
            else:
                print("* {} | {} | {} *".format(self.board[3 * row],
                                                self.board[3 * row + 1],
                                                self.board[3 * row + 2]))
            if row < 2:
                print("*-----------*")
        print("*************")

    def _check_victory(self, player_symbol: str) -> bool:
        # Checks if the last player to move has won by checking all possible
        # winning combinations.
        victory = False
        for combination in self.winning_combinations:
            victory = victory or self._three_in_a_row(combination,
                                                      player_symbol)
            if victory:
                break
        return victory

    def _three_in_a_row(self, combination: tuple[int, int, int],
                        player_symbol: str) -> bool:
        for position in combination:
            if self.board[position] != player_symbol:
                return False
        return True