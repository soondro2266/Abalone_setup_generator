def is_valid(x: int, y: int, n: int):
    return not (
        x < 0 
        or y < 0 
        or x >= (2*n - 1) 
        or y >= (2*n - 1) 
        or x-y >= n 
        or x-y <= -n
    )

def oneD_to_twoD(state: str, n: int):
    state_ = [[-1 for _ in range(9)] for _ in range(9)]
    cnt = 0
    for i in range(2*n-1):
        for j in range(2*n-1):
            if is_valid(i, j):
                state_[i, j] = state[cnt]
                cnt += 1
    return state_


def readGameRecord():

    with open("./gameRecord.txt") as file:
        records = file.readlines()

    train_data = []
    train_label = []
    for record in records:
        state, action = record.replace('\n', '').split(" ")
        state = oneD_to_twoD(state)
        train_data.append(state)
        train_label.append(action)
        
    return train_data, train_label