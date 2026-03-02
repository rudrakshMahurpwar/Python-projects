import os


def display_board(board):
    os.system("cls")
    for i in range(3):
        row = board[i * 3 : (i + 1) * 3]
        print(" {} | {} | {} ".format(*row))
        if i < 2:
            print("-----------")


def player_move(board, player):
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): "))
            if 1 <= move <= 9:
                move -= 1
                if board[move] == " ":
                    return move
                else:
                    print("Already Occupied")
            else:
                print("Out of Range")

        except ValueError:
            print("Enter an integer")


def check_winner(board, player):
    winning_conditions = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    for a, b, c in winning_conditions:
        if board[a] == board[b] == board[c] == player:
            return True

    return False


def draw(board):
    return " " not in board


def play(board, player):
    position = player_move(board, player)
    board[position] = player
    display_board(board)


if __name__ == "__main__":
    board = [" "] * 9

    print("Positions are numbered 1 to 9 as below:")
    print(" 1 | 2 | 3 ")
    print("-----------")
    print(" 4 | 5 | 6 ")
    print("-----------")
    print(" 7 | 8 | 9 \n")

    display_board(board)
    player = "X"

    while True:
        play(board, player)

        if check_winner(board, player):
            print(f"Player {player} Won.")
            display_board(board)
            break

        if draw(board):
            print("Game Draw")
            break

        player = "O" if player == "X" else "X"
