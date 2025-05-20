import numpy as np



class AbaloneEnv:
    def __init__(self, n = 5, white_state:list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15]\
                 , black_state:list[int] = [56, 57, 58, 50, 51, 52, 53, 54, 55, 45, 46, 47, 59, 60], score = 6):
        
        self.number_of_edge = n
        self.size_of_matrix = 2*n-1
        self.number_of_place = 3 * n * (n - 1) + 1
        self.directions = [[0, 1], [1, 1], [1, 0], [0, -1], [-1, -1], [-1, 0]]
        self.oneD_to_twoD:list[tuple[int, int]] = []
        self.white: np.ndarray = np.zeros((2*n-1, 2*n-1), dtype=bool)
        self.black: np.ndarray = np.zeros((2*n-1, 2*n-1), dtype=bool)
        self.valid: np.ndarray = np.zeros((2*n-1, 2*n-1), dtype=bool)
        self.player:bool = False
        """
        False : player is white
        True : player is black
        """
        self.score = score
        self.white_score = 0
        self.black_score = 0
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
        for oneD in range(self.number_of_place):
            if not self._is_ally(self.oneD_to_twoD[oneD]):
                continue
            for direction in range(6):
                position:list[tuple[int, int]] = []
                position.append(self.oneD_to_twoD[oneD])
                for _ in range(5):
                    position.append((position[-1][0]+self.directions[direction][0], position[-1][1]+self.directions[direction][1]))
                side_move_position_1 = []
                side_move_position_2 = []
                for i in range(3):
                    side_move_position_1.append((position[i][0]+self.directions[(direction+5)%6][0],\
                                                 position[i][1]+self.directions[(direction+5)%6][1]))
                    side_move_position_2.append((position[i][0]+self.directions[(direction+1)%6][0],\
                                                 position[i][1]+self.directions[(direction+1)%6][1]))
                if self._is_ally(position[1]):
                    if self._is_empty(side_move_position_1[0]) and\
                       self._is_empty(side_move_position_1[1]): #two side move second direction -1
                        actions.append(oneD*42+1*6+direction)
                    if self._is_empty(side_move_position_2[0]) and\
                       self._is_empty(side_move_position_2[1]): #two side move second direction 1
                        actions.append(oneD*42+3*6+direction)
                    if self._is_ally(position[2]):
                        if self._is_empty(side_move_position_1[0]) and\
                           self._is_empty(side_move_position_1[1]) and\
                           self._is_empty(side_move_position_1[2]) : #three side move second direction -1
                            actions.append(oneD*42+4*6+direction)
                        if self._is_empty(side_move_position_2[0]) and\
                           self._is_empty(side_move_position_2[1]) and\
                           self._is_empty(side_move_position_2[2]) : #three side move second direction -1
                            actions.append(oneD*42+6*6+direction)
                        if self._is_empty(position[3]):#three to empty
                            actions.append(oneD*42+5*6+direction)
                        elif self._is_enemy(position[3]):
                            if(self._is_empty(position[4]) or not self._is_valid(position[4])): #three push one
                                actions.append(oneD*42+5*6+direction)
                            elif self._is_enemy(position[4]) and (self._is_empty(position[5]) or not self._is_valid(position[5])):#three push two
                                actions.append(oneD*42+5*6+direction)
                    elif self._is_enemy(position[2]) and (self._is_empty(position[3]) or not self._is_valid(position[3])):#two push one
                        actions.append(oneD*42+2*6+direction)
                    elif self._is_empty(position[2]): #two to empty
                        actions.append(oneD*42+2*6+direction)
                elif self._is_empty(position[1]): #one to empty
                    actions.append(oneD*42+direction)
        return actions


    def reset(self):
        # 重置遊戲，回傳初始 state
        self.finished = False
        return self.state

    def step(self, action:int):

        oneDpos:int = action // 42
        remainder = action % 42
        type:int = remainder // 6
        direction = remainder % 6

        number_of_piece = 0
        second_direction = 0
        if type == 0:
            number_of_piece = 1
            second_direction = 0
        elif type == 1:
            number_of_piece = 2
            second_direction = -1
        elif type == 2:
            number_of_piece = 2
            second_direction = 0
        elif type == 3:
            number_of_piece = 2
            second_direction = 1
        elif type == 4:
            number_of_piece = 3
            second_direction = -1
        elif type == 5:
            number_of_piece = 3
            second_direction = 0
        elif type == 6:
            number_of_piece = 3
            second_direction = 1

        ally  = self.black if self.player else self.white
        enemy = self.white if self.player else self.black

        if second_direction == 0:
            ally_first = self.oneD_to_twoD[oneDpos]
            next_first = (ally_first[0]+number_of_piece*self.directions[direction][0], 
                         ally_first[1]+number_of_piece*self.directions[direction][1])
            
            next_last_plus_one = next_first
            
            while self._is_enemy(next_last_plus_one):
                next_last_plus_one = (next_last_plus_one[0]+self.directions[direction][0], 
                                      next_last_plus_one[1]+self.directions[direction][1])
            
            ally[ally_first] = False
            ally[next_first] = True
            enemy[next_first] = False
            if self._is_empty(next_last_plus_one):
                enemy[next_last_plus_one] = True
            else:
                if self.player:
                    self.black_score += 1
                else:
                    self.white_score += 1

        else:
            position:list[tuple[int, int]] = []
            target_position:list[tuple[int, int]] = []
            position.append(self.oneD_to_twoD[oneDpos])
            for _ in range(number_of_piece-1):
                position.append((position[-1][0]+self.directions[direction][0], position[-1][1]+self.directions[direction][1]))
            for i in range(number_of_piece):
                target_position.append((position[i][0]+self.directions[(direction+second_direction+6)%6][0],\
                                        position[i][1]+self.directions[(direction+second_direction+6)%6][1]))
            for i in range(number_of_piece):
                ally[position[i]] = False
                ally[target_position[i]] = True


        self.player = not self.player      

        self.finished = self._check_done()
        
        if self.finished:
            reward = self._who_won()
        else:
            reward = 0
        
        return self.get_state_tensor(), reward, self.finished
    

    def _check_done(self):
        # … 判斷遊戲是不是結束 …
        return True or False

    def _who_won(self):
        # … 根據最終局面決定 +1 or -1 …
        return +1 or -1
    
    def get_state_tensor(self) -> np.ndarray:
        """
        Return a float32 NumPy array of shape (4, size_of_matrix, size_of_matrix) with four channels:
        - Channel 0: white stones (self.white)
        - Channel 1: black stones (self.black)
        - Channel 2: valid move mask (self.valid)
        - Channel 3: current player indicator (all entries set to -1 if the current player is white, +1 otherwise)
        """
        s_white = self.white.astype(np.float32)  # shape (size, size)
        s_black = self.black.astype(np.float32)  # shape (size, size)
        s_valid = self.valid.astype(np.float32)  # shape (size, size)

        fill = 1.0 if self.player else -1.0
        s_player = np.full(
            (self.size_of_matrix, self.size_of_matrix),
            fill,
            dtype=np.float32
        )

        state_tensor = np.stack([s_white, s_black, s_valid, s_player], axis=0)
        return state_tensor

    def _is_valid(self, position:tuple[int, int])->bool:
        if  position[0] < 0 or\
            position[1] < 0 or\
            position[0] >= 2 * self.number_of_edge - 1 or\
            position[1] >= 2 * self.number_of_edge - 1 or\
            position[0] - position[1] >=  self.number_of_edge or\
            position[0] - position[1] <= -self.number_of_edge:
            return False
        return True
    
    def _is_empty(self, position)->bool:
        if not self._is_valid(position):
            return False
        return not (self.white[position[0]][position[1]] or self.black[position[0]][position[1]])

    def _is_white(self, position)->bool:
        if not self._is_valid(position):
            return False
        return self.white[position[0]][position[1]]
    
    def _is_black(self, position)->bool:
        if not self._is_valid(position):
            return False
        return self.black[position[0]][position[1]]
    
    def _is_ally(self, position)->bool:
        if self.player:
            return self._is_black(position)
        else:
            return self._is_white(position)
    
    def _is_enemy(self, position)->bool:
        if not self.player:
            return self._is_black(position)
        else:
            return self._is_white(position)
        
    def _check_done(self)->bool:
        return self.white_score >= self.score or self.black_score >= self.score
    
    def _who_won(self)->int:
        return 1 if self.white_score >- self.score else -1