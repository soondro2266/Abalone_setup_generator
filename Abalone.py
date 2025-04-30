


class Hex:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.direction_tuple:list[tuple[int, int]] = [(0, 1), (1, 1), (1, 0), (0, -1), (-1, -1), (-1, 0)]
    
    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def move(self, direction):
        self.x += self.direction_tuple[direction][0]
        self.y += self.direction_tuple[direction][1]
    

class Abalone:
    def __init__(self, n = 5, pieces = 14, end_pieces = 6):
        self.n = n
        self.pieces = 14
        self.end_pieces = end_pieces
        self.board = {}

    def load_board_from_dict(self, board:dict):
        self.board = board
    
    def load_default_board(self):
        self.board = {
            True:[Hex(0, 0),Hex(0, 1),Hex(0, 2),Hex(0, 3),Hex(0, 4),
                  Hex(1, 0),Hex(1, 1),Hex(1, 2),Hex(1, 3),Hex(1, 4),Hex(1, 5),
                  Hex(2, 2),Hex(2, 3),Hex(2, 4)],
            False:[Hex(8, 4),Hex(8, 5),Hex(8, 6),Hex(8, 7),Hex(8, 8),
                   Hex(7, 3),Hex(7, 4),Hex(7, 5),Hex(7, 6),Hex(7, 7),Hex(1, 8),
                   Hex(6, 4),Hex(6, 5),Hex(6, 6)]
        }

    def is_valid(self, position:Hex):
        if position.x < 0 or position.y < 0:
            return False
        if position.x >= 2*self.n - 1 or position.y >= 2*self.n - 1:
            return False
        if position.x-position.y >= self.n or position.x-position.y <= -self.n:
            return False
        return True