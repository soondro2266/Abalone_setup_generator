import copy

    
class Board:
    def __init__(self, n = 5, pieces = 14):
        self.n = n
        self.pieces = pieces
        self.white = set()
        self.black = set()
        self.direction_tuple:list[tuple[int, int]] = [(0, 1), (1, 1), (1, 0), (0, -1), (-1, -1), (-1, 0)]

    def __deepcopy__(self, memo):
        new_board = Board.__new__(Board)

        memo[id(self)] = new_board

        new_board.n = copy.deepcopy(self.n, memo)
        new_board.pieces = copy.deepcopy(self.pieces, memo)
        new_board.white = copy.deepcopy(self.white, memo)
        new_board.black = copy.deepcopy(self.black, memo)

        new_board.direction_tuple = self.direction_tuple

        return new_board

    def load_board_from_dict(self, board:dict):
        self.white.clear()
        self.black.clear()
        for piece in board[True]:
            self.white.add(piece)
        for piece in board[False]:
            self.black.add(piece)
    
    def load_default_board(self):
        self.white.clear()
        self.black.clear()
        self.white = {
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
            (2, 2), (2, 3), (2, 4)
        }
        self.black = {
            (8, 4), (8, 5), (8, 6), (8, 7), (8, 8),
            (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8),
            (6, 4), (6, 5), (6, 6)
        }
    
    def is_empty(self, pos):
        return pos not in self.white and pos not in self.black
    
    def is_white(self, pos):
        return pos in self.white
    
    def is_black(self, pos):
        return pos in self.black

    def is_valid(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= 2*self.n - 1 or pos[1] >= 2*self.n - 1:
            return False
        if pos[0]-pos[1] >= self.n or pos[0]-pos[1] <= -self.n:
            return False
        return True

    def all_next_move(self, player=True):
        return (
            self.all_next_move_one_piece(player) +
            self.all_next_move_two_piece(player) +
            self.all_next_move_three_piece(player) +
            self.all_inline_push_two_piece(player) + 
            self.all_inline_push_three_piece(player)
        )
    
    def all_next_move_String(self, player=True):
        return (
            self.convert_to_String(self.all_next_move_one_piece(player)) +
            self.convert_to_String(self.all_next_move_two_piece(player)) +
            self.convert_to_String(self.all_next_move_three_piece(player)) +
            self.convert_to_String(self.all_inline_push_two_piece(player)) + 
            self.convert_to_String(self.all_inline_push_three_piece(player))
        )
    
    # convert to string + action
    def convert_to_String(all_board: list):
        


    def load_from_String(self, str: str):
        self.white = []
        self.black = []

        for i in range(len(str)):
            # white
            if int(str[i]) == 1:
                self.white.append((i//9)-1, i%9)
            #black    
            elif int(str[i]) == 2:
                self.black.append((i//9)-1, i%9)


    def get_perpendicular_directions(self, direction):
        idx = self.direction_tuple.index(direction)
        # 六個方向圍成環狀，垂直的兩個方向在±2 位置上
        pera1 = self.direction_tuple[(idx + 2) % 6]
        pera2 = self.direction_tuple[(idx - 2) % 6]
        return [pera1, pera2]
    
    def all_next_move_one_piece(self, player=True):
        all_board = []
        pieces = self.white if player else self.black

        for piece in pieces:
            for direction in self.direction_tuple:
                next_pos = (piece[0] + direction[0], piece[1] + direction[1])
                if self.is_valid(next_pos) and self.is_empty(next_pos):
                    new_board = copy.deepcopy(self)
                    target_set = new_board.white if player else new_board.black
                    target_set.remove(piece)
                    target_set.add(next_pos)
                    all_board.append(new_board)

        return all_board

    def all_next_move_two_piece(self, player=True):
        all_board = []
        pieces = self.white if player else self.black

        for a1 in pieces:
            for direction in self.direction_tuple:
                a2 = (a1[0] + direction[0], a1[1] + direction[1])
                if a2 in pieces:
                    # 找到一對相鄰棋子
                    # 接著找與原方向垂直的 sidestep 方向
                    perp_directions = self.get_perpendicular_directions(direction)
                    for move_direction in perp_directions:
                        na1 = (a1[0] + move_direction[0], a1[1] + move_direction[1])
                        na2 = (a2[0] + move_direction[0], a2[1] + move_direction[1])
                        if self.is_valid(na1) and self.is_valid(na2) and self.is_empty(na1) and self.is_empty(na2):
                            new_board = copy.deepcopy(self)
                            target_set = new_board.white if player else new_board.black
                            target_set.remove(a1)
                            target_set.remove(a2)
                            target_set.add(na1)
                            target_set.add(na2)
                            all_board.append(new_board)

        return all_board

    def all_next_move_three_piece(self, player=True):
        all_board = []
        pieces = self.white if player else self.black

        for a1 in pieces:
            for direction in self.direction_tuple:
                a2 = (a1[0] + direction[0], a1[1] + direction[1])
                a3 = (a2[0] + direction[0], a2[1] + direction[1])
                if a2 in pieces and a3 in pieces:
                    # 找到三顆連線的棋子
                    perp_directions = self.get_perpendicular_directions(direction)
                    for move_direction in perp_directions:
                        na1 = (a1[0] + move_direction[0], a1[1] + move_direction[1])
                        na2 = (a2[0] + move_direction[0], a2[1] + move_direction[1])
                        na3 = (a3[0] + move_direction[0], a3[1] + move_direction[1])
                        if all(self.is_valid(p) and self.is_empty(p) for p in [na1, na2, na3]):
                            new_board = copy.deepcopy(self)
                            target_set = new_board.white if player else new_board.black
                            target_set.difference_update({a1, a2, a3})
                            target_set.update({na1, na2, na3})
                            all_board.append(new_board)

        return all_board
                
    def all_inline_push_two_piece(self, player=True):
        all_board = []
        ally = self.white if player else self.black
        enemy = self.black if player else self.white

        for a1 in ally:
            for direction in self.direction_tuple:
                a2 = (a1[0] + direction[0], a1[1] + direction[1])
                if a2 not in ally:
                    continue  # 兩子不相連，略過

                # 嘗試 push
                e1= (a2[0] + direction[0], a2[1] + direction[1])

                if e1 in enemy:
                    e2 = (e1[0] + direction[0], e1[1] + direction[1])
                    # Ally Ally Enemy Blank
                    if self.is_valid(e2) and self.is_empty(e2):
                        new_board = copy.deepcopy(self)
                        a_set = new_board.white if player else new_board.black
                        e_set = new_board.black if player else new_board.white

                        # 推進
                        a_set.remove(a1)
                        a_set.add(e1)

                        e_set.remove(e1)
                        e_set.add(e2)

                        all_board.append(new_board)

                    # Ally Ally Enemy X(invalid)
                    elif not self.is_valid(e2):
                        # 推出場外也合法
                        new_board = copy.deepcopy(self)
                        a_set = new_board.white if player else new_board.black
                        e_set = new_board.black if player else new_board.white

                        a_set.remove(a1)
                        a_set.add(e1)

                        e_set.remove(e1)

                        all_board.append(new_board)

                # Ally Ally Blank
                elif self.is_empty(e1) and self.is_valid(e1):
                    new_board = copy.deepcopy(self)
                    a_set = new_board.white if player else new_board.black

                    a_set.remove(a1)
                    a_set.add(e1)

                    all_board.append(new_board)

        return all_board
    
    def all_inline_push_three_piece(self, player=True):
        all_board = []
        ally = self.white if player else self.black
        enemy = self.black if player else self.white

        for a1 in ally:
            for direction in self.direction_tuple:
                a2 = (a1[0] + direction[0], a1[1] + direction[1])
                a3 = (a2[0] + direction[0], a2[1] + direction[1])
                if a2 in ally and a3 in ally:
                    # 接下來就是看能不能推一或兩顆敵子
                    e1 = (a3[0] + direction[0], a3[1] + direction[1])
                    e2 = (e1[0] + direction[0], e1[1] + direction[1])

                    if e1 in enemy:
                        if e2 in enemy:
                            # 3 推 2
                            e3 = (e2[0] + direction[0], e2[1] + direction[1])
                            if not self.is_valid(e3):
                                # 推出界外（合法）
                                new_board = copy.deepcopy(self)
                                a_set = new_board.white if player else new_board.black
                                e_set = new_board.black if player else new_board.white

                                a_set.remove(a1)
                                a_set.add(e1)
                                e_set.remove(e1)
                                all_board.append(new_board)

                            elif self.is_valid(e3) and self.is_empty(e3):
                                # 推入空格（合法）
                                new_board = copy.deepcopy(self)
                                a_set = new_board.white if player else new_board.black
                                e_set = new_board.black if player else new_board.white

                                a_set.remove(a1)
                                a_set.add(e1)
                                e_set.remove(e1)
                                e_set.add(e3)
                                all_board.append(new_board)
                        else:
                            # 3 推 1
                            if self.is_valid(e2) and self.is_empty(e2):
                                new_board = copy.deepcopy(self)
                                a_set = new_board.white if player else new_board.black
                                e_set = new_board.black if player else new_board.white

                                a_set.remove(a1)
                                a_set.add(e1)
                                e_set.remove(e1)
                                e_set.add(e2)
                                all_board.append(new_board)
                            elif not self.is_valid(e2):
                                # 推出界外
                                new_board = copy.deepcopy(self)
                                a_set = new_board.white if player else new_board.black
                                e_set = new_board.black if player else new_board.white

                                a_set.remove(a1)
                                a_set.add(e1)
                                e_set.remove(e1)
                                all_board.append(new_board)

                    # 3 推 0
                    elif self.is_empty(e1) and self.is_valid(e1):
                        new_board = copy.deepcopy(self)
                        a_set = new_board.white if player else new_board.black

                        a_set.remove(a1)
                        a_set.add(e1)
                        all_board.append(new_board)

        return all_board
    
    def show(self):
        board = [
            ['*', '*', '*', '*', '*', ' ', ' ', ' ', ' '],
            ['*', '*', '*', '*', '*', '*', ' ', ' ', ' '],
            ['*', '*', '*', '*', '*', '*', '*', ' ', ' '],
            ['*', '*', '*', '*', '*', '*', '*', '*', ' '],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
            [' ', '*', '*', '*', '*', '*', '*', '*', '*'],
            [' ', ' ', '*', '*', '*', '*', '*', '*', '*'],
            [' ', ' ', ' ', '*', '*', '*', '*', '*', '*'],
            [' ', ' ', ' ', ' ', '*', '*', '*', '*', '*'],
        ]
        
        for w in self.white:
            board[w[0]][w[1]] = 'W'
        for b in self.black:
            board[b[0]][b[1]] = 'B'

        board[0] = ['', '', '', ''] + board[0][:5]
        board[1] = ['', '', ''] + board[1][:6]
        board[2] = ['', ''] + board[2][:7]
        board[3] = [''] + board[3][:8]
        board[8] = ['', '', '', ''] + board[8][4:]
        board[7] = ['', '', ''] + board[7][3:]
        board[6] = ['', ''] + board[6][2:]
        board[5] = [''] + board[5][1:]

        for row in board:
            for block in row:
                print(block, end = ' ')
            print("")    