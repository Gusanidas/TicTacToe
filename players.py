# Module with different player classes.

import time
from random import randint
from enum import Enum


# Parent class for the different players.
class Player:

    def __init__(self, symbol: str):
        self.symbol = symbol

    def move(self, board: list[str]) -> int:
        pass


# Chooses valid moves at random.
class RandomPlayer(Player):

    def move(self, board: list[str]) -> int:
        time.sleep(0.3)
        legal_moves = []
        for position, value in enumerate(board):
            if value == " ":
                legal_moves.append(position)
        if len(legal_moves) <= 0:
            return None
        return legal_moves[randint(0, len(legal_moves) - 1)]


# Ask for the next move in the input and cheks its validity.
class HumanPlayer(Player):

    def move(self, board: list[str]) -> int:
        print("Player {} turn".format(self.symbol))
        while True:
            move = input("What is your move? ")
            valid, msg = self._check_valid_move(move, board)
            if valid:
                break
            else:
                print(msg)
                print("Try again")
        return int(move) - 1

    def _check_valid_move(self, move: str,
                          board: list[str]) -> tuple[bool, str]:
        try:
            move = int(move)
        except ValueError:
            return False, "Position must be an int between 1 and 9"
        if move < 1 or move > 9:
            return False, "Choose a number between 1 and 9"
        if board[move - 1] != " ":
            return False, "That position is already occupied"
        return True, ""


# Implements the Minimax algorithm
class MinimaxPlayer(Player):

    # All scores will be between these values.
    MIN_SCORE = -20000
    MAX_SCORE = 20000

    class Phase(Enum):
        MIN = 1
        MAX = 2

    def __init__(self, symbol: str, symbol_opponent: str, max_depth: int = 6):
        super().__init__(symbol)
        self.symbol_opponent = symbol_opponent
        self.max_depth = max_depth

        self.winning_combinations = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6))
        # Score map of a combination based on the pair (no of cells occupied
        # by the player, number of blanks cells).
        self.scores = {(2, 1): 200, # eg: ["O", " ", "O"]
                       (1, 2): 20, # eg: [" ", " ", "O"]
                       (0, 3): 0, # eg: [" ", " ", " "]
                       (1, 1): 0, # eg: ["O", "X", " "]
                       (2, 0): 0, # eg: ["O", "O", "X"]
                       (1, 0): 0, # eg: ["O", "X", "X"]
                       (0, 1): -20, # eg: [" ", "X", " "]
                       (0, 2): -200} # eg: [" ", "X", "X"]

    def move(self, board: list[str]) -> int:
        time.sleep(0.3)
        _, new_position = self._rate_move(board, self.MAX_SCORE, 0,
                                          self.Phase.MAX)
        return new_position

    def _rate_move(self, board: list[str], prune: int, depth: int,
                   phase: "MinimaxPlayer.Phase") -> tuple[int, int]:
        if self._is_victory(board, self.symbol):
            return 10000, None
        if self._is_victory(board, self.symbol_opponent):
            return -10000, None
        if depth == self.max_depth:
            return self._rate_board(board), None
        if board.count(" ") == 0:
            return 0, None

        if phase == self.Phase.MAX:
            max_score, max_position = self.MIN_SCORE, None
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.symbol
                    score, _ = self._rate_move(board, max_score, depth + 1,
                                               self.Phase.MIN)
                    board[i] = " "
                    if score > max_score:
                        max_score, max_position = score, i
                        if max_score > prune:
                            break

            return max_score, max_position
        else:
            min_score, min_position = self.MAX_SCORE, None
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.symbol_opponent
                    score, _ = self._rate_move(board, min_score, depth + 1,
                                               self.Phase.MAX)
                    board[i] = " "
                    if score < min_score:
                        min_score, min_position = score, i
                        if min_score < prune:
                            break
            return min_score, min_position

    def _is_victory(self, board: list[str], symbol: str) -> bool:
        victory = False
        for combination in self.winning_combinations:
            victory = victory or self._three_in_a_row(board, combination,
                                                      symbol)
        return victory

    def _three_in_a_row(self, board: list[str],
                        combination: tuple[int, int, int],
                        symbol: str) -> bool:
        for position in combination:
            if board[position] != symbol:
                return False
        return True
    
    def _rate_board(self, board: list[str]) -> int:
        score = 0
        for combination in self.winning_combinations:
            score += self._rate_combination(board, combination)
        return score

    def _rate_combination(self, board: list[str],
                          combination: tuple[int, int, int]):
        symbol_count, blank_count = 0, 0
        for position in combination:
            if board[position] == self.symbol:
                symbol_count += 1
            elif board[position] == " ":
                blank_count += 1

        return self.scores[(symbol_count, blank_count)]
