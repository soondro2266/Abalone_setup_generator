import os


def is_valid(x: int, y: int, n: int):
    return not (
        x < 0 
        or y < 0 
        or x >= (2*n - 1) 
        or y >= (2*n - 1) 
        or x-y >= n 
        or x-y <= -n
    )

def is_empty(label: int):
    return label == 0

def is_white(label: int):
    return label == 1

def is_black(label: int):
    return label == 2

def oneD_to_twoD(state: str, n: int, player: int):
    state_ = []
    # white board
    white_board = [[0 for _ in range(2*n-1)] for _ in range(2*n-1)]
    # black board
    black_board = white_board
    # take turn board 1 stand for next move is provided by black, -1 for white
    takeTurn_board = [[player for _ in range(2*n-1)] for _ in range(2*n-1)]
    # valid board
    valid_board = white_board

    cnt = 0
    for i in range(2*n-1):
        for j in range(2*n-1):
            if is_valid(i, j, n):
                valid_board[i][j] = 1
                if is_white(state[cnt]):
                    white_board[i][j] = 1
                elif is_black(state[cnt]):
                    black_board[i][j] = 1

    state_.append(white_board)
    state_.append(black_board)
    state_.append(takeTurn_board)
    state_.append(valid_board)

    return state_


def readGameRecord(n: int):

    train_data = []
    train_label = []

    for result in os.listdir("./minmax_results"):
        with open("./minmax_results/"+result) as file:
            records = file.readlines()
            
        player = 1
        
        # extract first state and last action
        first_state, _ = records[0].replace('\n', '').split(" ")
        _, last_action = records[-1].replace('\n', '').split(" ")

        # append first state
        first_state = oneD_to_twoD(first_state, n, player)
        train_data.append(first_state)

        # get rid of last data (since last action is extracted)
        records.pop()

        for record in records[1:]:
            player *= -1
            state, action = record.replace('\n', '').split(" ")
            state = oneD_to_twoD(state, n, player)
            action = int(action)
            train_data.append(state)
            train_label.append(action)

        # append last action
        last_action = int(last_action)
        train_label.append(last_action)
        
    return train_data, train_label