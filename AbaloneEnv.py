import numpy as np



class AbaloneEnv:
    def __init__(self, n = 5, white_state:list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15]\
                 , black_state:list[int] = [56, 57, 58, 50, 51, 52, 53, 54, 55, 45, 46, 47, 59, 60]):
        
        self.number_of_edge = n
        self.size_of_matrix = 2*n-1
        self.number_of_place = 3 * n * (n - 1) + 1
        self.directions = [[0, 1], [1, 1], [1, 0], [0, -1], [-1, -1], [-1, 0]]
        self.oneD_to_twoD:list[tuple[int, int]] = []
        self.white: np.ndarray = np.zeros((2*n-1, 2*n-1), dtype=bool)
        self.black: np.ndarray = np.zeros((2*n-1, 2*n-1), dtype=bool)
        self.valid: np.ndarray = np.zeros((2*n-1, 2*n-1), dtype=bool)
        self.player:bool = False
        self.white_pieces = len(white_state)
        self.black_pieces = len(black_state)
        for i in range(2*n-1):
            for j in range(2*n-1):
                position = (i, j)
                if self._is_valid(position):
                    self.oneD_to_twoD.append(position)
                    self.valid[i][j] = True
        
        for oneD in white_state:
            position = self.oneD_to_twoD[oneD]
            self.white[position[0]][position[1]] = True
        for oneD in black_state:
            position = self.oneD_to_twoD[oneD]
            self.black[position[0]][position[1]] = True
        pass

    def get_all_actions(self):
        actions:list[int] = []
        ally  = self.black if self.player else self.white
        enemy = self.white if self.player else self.black
        empty = np.logical_and(self.valid, np.logical_not(np.logical_or(self.black, self.white)))
        for oneD in range(self.number_of_place):
            position:list[tuple[int, int]] = []
            position.append(self.oneD_to_twoD[oneD])
            if not ally[position[0]]:
                continue
            for direction in range(6):
                for _ in range(5):
                    position.append((position[-1][0]+self.directions[direction][0], position[-1][1]+self.directions[direction][1]))
                side_move_position_1 = []
                side_move_position_2 = []
                for i in range(3):
                    side_move_position_1.append((position[i][0]+self.directions[(direction+5)%6][0],\
                                                 position[i][1]+self.directions[(direction+5)%6][1]))
                    side_move_position_2.append((position[i][0]+self.directions[(direction+1)%6][0],\
                                                 position[i][1]+self.directions[(direction+1)%6][1]))
                if ally[position[1]]:
                    if empty[side_move_position_1[0]] and\
                       empty[side_move_position_1[1]]: #two side move second direction -1
                        actions.append(oneD*42+1*6+direction)
                    if empty[side_move_position_2[0]] and\
                       empty[side_move_position_2[1]]: #two side move second direction 1
                        actions.append(oneD*42+3*6+direction)
                    if ally[position[2]]:
                        if empty[side_move_position_1[0]] and\
                           empty[side_move_position_1[1]] and\
                           empty[side_move_position_1[2]] : #three side move second direction -1
                            actions.append(oneD*42+4*6+direction)
                        if empty[side_move_position_2[0]] and\
                           empty[side_move_position_2[1]] and\
                           empty[side_move_position_2[2]] : #three side move second direction -1
                            actions.append(oneD*42+6*6+direction)
                        if empty[position[3]]:#three to empty
                            actions.append(oneD*42+5*6+direction)
                        elif enemy[position[3]]:
                            if(empty[position[4]] or not self.valid[position[4]]): #three push one
                                actions.append(oneD*42+5*6+direction)
                            elif enemy[position[4]] and (empty[position[5]] or not self.valid[position[5]]):#three push two
                                actions.append(oneD*42+5*6+direction)
                    elif enemy[position[2]] and (empty[position[3]] or not self.valid[position[3]]):#two push one
                        actions.append(oneD*42+2*6+direction)
                    elif empty[position[2]]: #two to empty
                        actions.append(oneD*42+2*6+direction)
                elif empty[position[1]]: #one to empty
                    actions.append(oneD*42+direction)
        return actions      


    def reset(self):
        # 重置遊戲，回傳初始 state
        self.finished = False
        return self.state

    def step(self, action):
        # 1) 套用 action，更新 self.state
        # 2) 檢查遊戲是否結束
        self.finished = self._check_done()
        
        # 3) 設定 reward
        if self.finished:
            # 假設 self._who_won() 回傳 +1（玩家勝）或 -1（玩家負）
            reward = self._who_won()
        else:
            reward = 0
        
        # 4) 回傳四元組
        #    next_state, reward, done, info
        return self.state, reward, self.finished, {}
    
    def _check_done(self):
        # … 判斷遊戲是不是結束 …
        return True or False

    def _who_won(self):
        # … 根據最終局面決定 +1 or -1 …
        return +1 or -1
    
    def _is_valid(self, position):
        if  position[0] < 0 or\
            position[1] < 0 or\
            position[0] >= 2 * self.number_of_edge - 1 or\
            position[1] >= 2 * self.number_of_edge - 1 or\
            position[0] - position[1] >=  self.number_of_edge or\
            position[0] - position[1] <= -self.number_of_edge:
            return False
        return True