# Main class for the game, asks the user about the type of game they
# want to play and sets it up.

 
from game import Game
from players import HumanPlayer, RandomPlayer, MinimaxPlayer


def get_one_or_two():
    while True:
        choice = input("1/2: ")
        if choice in ("1", "2"):
            break
        else:
            print("Invalid input, please enter 1 or 2.")
    return choice


def game_loop():
    while True:
        print("Do you want to: ")
        print("  1 - Play against a friend")
        print("  2 - Play against the computer")
        choice = get_one_or_two()

        player1 = HumanPlayer("X")
        if choice == "1":
            player2 = HumanPlayer("O")
            game = Game(player1, player2)
        else:
            print("Choose the difficulty")
            print("  1 - Easy")
            print("  2 - Medium")
            print("  3 - Difficult")
            while True:
                choice = input("1/2/3: ")
                if choice in ("1", "2", "3"):
                    break
                else:
                    print("Invalid input, please enter 1, 2 or 3.")

            if choice == "1":
                player2 = RandomPlayer("O")
            elif choice == "2":
                player2 = MinimaxPlayer("O", "X", max_depth=2)
            else:
                player2 = MinimaxPlayer("O", "X")

            print("Do you want to: ")
            print("  1 - Go first")
            print("  2 - Go second")
            choice = get_one_or_two()

            if choice == "1":
                game = Game(player1, player2)
            else:
                game = Game(player2, player1)

        game.start()

        print("Do you want to play again?")
        print("  1 - Yes")
        print("  2 - No")
        choice = get_one_or_two()

        if choice == "2":
            print("See you soon!")
            break


if __name__ == "__main__":
    game_loop()

                    