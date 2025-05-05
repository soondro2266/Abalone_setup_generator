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
            (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (1, 8),
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

    def get_perpendicular_dirs(self, dir):
        idx = self.direction_tuple.index(dir)
        # 六個方向圍成環狀，垂直的兩個方向在±2 位置上
        perp1 = self.direction_tuple[(idx + 2) % 6]
        perp2 = self.direction_tuple[(idx - 2) % 6]
        return [perp1, perp2]
    
    def all_next_move_one_piece(self, player=True):
        all_board = []
        pieces = self.white if player else self.black

        for piece in pieces:
            for dir in self.direction_tuple:
                next_pos = (piece[0] + dir[0], piece[1] + dir[1])
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

        for p1 in pieces:
            for dir in self.direction_tuple:
                p2 = (p1[0] + dir[0], p1[1] + dir[1])
                if p2 in pieces:
                    # 找到一對相鄰棋子
                    # 接著找與原方向垂直的 sidestep 方向
                    perp_dirs = self.get_perpendicular_dirs(dir)
                    for move_dir in perp_dirs:
                        np1 = (p1[0] + move_dir[0], p1[1] + move_dir[1])
                        np2 = (p2[0] + move_dir[0], p2[1] + move_dir[1])
                        if self.is_valid(np1) and self.is_valid(np2) and self.is_empty(np1) and self.is_empty(np2):
                            new_board = copy.deepcopy(self)
                            target_set = new_board.white if player else new_board.black
                            target_set.remove(p1)
                            target_set.remove(p2)
                            target_set.add(np1)
                            target_set.add(np2)
                            all_board.append(new_board)

        return all_board

    def all_next_move_three_piece(self, player=True):
        all_board = []
        pieces = self.white if player else self.black

        for p1 in pieces:
            for dir in self.direction_tuple:
                p2 = (p1[0] + dir[0], p1[1] + dir[1])
                p3 = (p2[0] + dir[0], p2[1] + dir[1])
                if p2 in pieces and p3 in pieces:
                    # 找到三顆連線的棋子
                    perp_dirs = self.get_perpendicular_dirs(dir)
                    for move_dir in perp_dirs:
                        np1 = (p1[0] + move_dir[0], p1[1] + move_dir[1])
                        np2 = (p2[0] + move_dir[0], p2[1] + move_dir[1])
                        np3 = (p3[0] + move_dir[0], p3[1] + move_dir[1])
                        if all(self.is_valid(p) and self.is_empty(p) for p in [np1, np2, np3]):
                            new_board = copy.deepcopy(self)
                            target_set = new_board.white if player else new_board.black
                            target_set.difference_update({p1, p2, p3})
                            target_set.update({np1, np2, np3})
                            all_board.append(new_board)

        return all_board
                
    def all_inline_push_two_piece(self, player=True):
        all_board = []
        ally = self.white if player else self.black
        enemy = self.black if player else self.white

        for p1 in ally:
            for dir in self.direction_tuple:
                p2 = (p1[0] + dir[0], p1[1] + dir[1])
                if p2 not in ally:
                    continue  # 兩子不相連，略過

                # 嘗試 push
                target = (p2[0] + dir[0], p2[1] + dir[1])

                if target in enemy:
                    beyond = (target[0] + dir[0], target[1] + dir[1])
                    if self.is_valid(beyond) and self.is_empty(beyond):
                        new_board = copy.deepcopy(self)
                        a_set = new_board.white if player else new_board.black
                        e_set = new_board.black if player else new_board.white

                        # 推進
                        a_set.remove(p1)
                        a_set.add(target)

                        e_set.remove(target)
                        e_set.add(beyond)

                        all_board.append(new_board)

                    elif not self.is_valid(beyond):
                        # 推出場外也合法
                        new_board = copy.deepcopy(self)
                        a_set = new_board.white if player else new_board.black
                        e_set = new_board.black if player else new_board.white

                        a_set.remove(p1)
                        a_set.add(target)

                        e_set.remove(target)

                        all_board.append(new_board)

        return all_board
    
    def all_inline_push_three_piece(self, player=True):
        all_board = []
        ally = self.white if player else self.black
        enemy = self.black if player else self.white

        for p1 in ally:
            for dir in self.direction_tuple:
                p2 = (p1[0] + dir[0], p1[1] + dir[1])
                p3 = (p2[0] + dir[0], p2[1] + dir[1])
                if p2 in ally and p3 in ally:
                    # 接下來就是看能不能推一或兩顆敵子
                    e1 = (p3[0] + dir[0], p3[1] + dir[1])
                    e2 = (e1[0] + dir[0], e1[1] + dir[1])

                    if e1 in enemy:
                        if e2 in enemy:
                            # 3 推 2
                            e3 = (e2[0] + dir[0], e2[1] + dir[1])
                            if not self.is_valid(e3):
                                # 推出界外（合法）
                                new_board = copy.deepcopy(self)
                                a_set = new_board.white if player else new_board.black
                                e_set = new_board.black if player else new_board.white

                                a_set.remove(p1)
                                a_set.add(e1)
                                e_set.remove(e1)
                                all_board.append(new_board)

                            elif self.is_valid(e3) and self.is_empty(e3):
                                # 推入空格（合法）
                                new_board = copy.deepcopy(self)
                                a_set = new_board.white if player else new_board.black
                                e_set = new_board.black if player else new_board.white

                                a_set.remove(p1)
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

                                a_set.remove(p1)
                                a_set.add(e1)
                                e_set.remove(e1)
                                e_set.add(e2)
                                all_board.append(new_board)
                            elif not self.is_valid(e2):
                                # 推出界外
                                new_board = copy.deepcopy(self)
                                a_set = new_board.white if player else new_board.black
                                e_set = new_board.black if player else new_board.white

                                a_set.remove(p1)
                                a_set.add(e1)
                                e_set.remove(e1)
                                all_board.append(new_board)

        return all_board
        