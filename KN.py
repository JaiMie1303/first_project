print("Игра 'Крестики - нолики'")

board = [" ", " ", " ",
         " ", " ", " ",
         " ", " ", " "]
player_1 = "X"
winner = None
game_running = True

def show_board(board):
    print("-"*9)
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("-"*9)
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("-" * 9)
    print(board[6] + " | " + board[7] + " | " + board[8])
    print("-" * 9)

def player_input(board):
    pnt = int(input("Введите цифру от 1-9: "))
    if pnt>=1 and pnt<=9 and board[pnt-1] == " ":
        board[pnt-1] = player_1
    else:
        print("Ячейка уже занята другим игроком")

def check_horizont(board):
    global winner
    if board[0] == board[1] == board[2] and board[1] != " ":
        winner = board[0]
        return True
    elif board[3] == board[4] == board[5] and board[3] != " ":
        winner = board[3]
        return True
    elif board[6] == board[7] == board[8] and board[6] != " ":
        winner = board[6]
        return True

def check_row(board):
    global winner
    if board[0] == board[3] == board[6] and board[0] != " ":
        winner = board[0]
        return True
    elif board[1] == board[4] == board[7] and board[1] != " ":
        winner = board[1]
        return True
    elif board[2] == board[5] == board[8] and board[2] != " ":
        winner = board[2]
        return True

def check_diag(board):
    global winner
    if board[0] == board[4] == board[8] and board[0] != " ":
        winner = board[0]
        return True
    elif board[2] == board[4] == board[6] and board[2] != " ":
        winner = board[2]
        return True

def check_tie(board):
    global game_running
    if " " not in board:
        show_board(board)
        print("Ничья!")
        game_running = False

def check_win():
    if check_diag(board) or check_horizont(board) or check_row(board):
        print(f"Выиграл {winner}")

def change_player():
    global player_1
    if player_1 == "X":
        player_1= "0"
    else:
        player_1 = "X"


while game_running:
    show_board(board)
    player_input(board)
    check_win()
    check_tie(board)
    change_player()

