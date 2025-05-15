#include <vector>
#include <map>
#define toWhite 1
#define toBlack 2
#define toEmpty 3
#define NextBoards vector<pair<pair<vector<bool>, vector<bool>>, int>>

using namespace std;

pair<int, int>& operator + (pair<int, int>& pos1, pair<int, int>& pos2){
    pair<int, int> result = {pos1.first + pos2.first, pos1.second + pos2.second};
    return result;
}


class Board
{
public:
    Board(){
        white = vector<bool>(61, 0);
        black = vector<bool>(61, 0);
    }

    auto get() -> pair<vector<bool>, vector<bool>>&{
        pair<vector<bool>, vector<bool>> board({white, black});
        return board;
    }
    void set(int state, int oneD_pos){
        switch(state){
            case 1:
                white[oneD_pos] = 1;
                break;
            case 2:
                black[oneD_pos] = 1;
                break;
            case 3:
                white[oneD_pos] = 0;
                black[oneD_pos] = 0;
                break;
        }
    }
    void show(){

    }

    bool is_empty(int oneD_pos){
        return white[oneD_pos] == 0 && black[oneD_pos] == 0;
    }
    bool is_white(int oneD_pos){
        return white[oneD_pos] == 1;
    }
    bool is_black(int oneD_pos){
        return black[oneD_pos] == 1;
    }
    bool is_valid(int x, int y, map<pair<int, int>, int>& mapping){
        return mapping.find({x, y}) != mapping.end();
    }

    auto get_current_board() -> pair<vector<bool>, vector<bool>>{
        return make_pair(white, black);
    }

private:
    vector<bool> white;
    vector<bool> black;
};

class AbaloneEnv
{
public:
    AbaloneEnv(){}

    void load_default_setup(){
        vector<int> defaultWhite = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15};
        vector<int> defaultBlack = {56, 57, 58, 50, 51, 52, 53, 54, 55, 45, 46, 47};
        for(int oneD_pos : defaultWhite){
            currentBoard.set(toWhite, oneD_pos);
        }
        for(int oneD_pos : defaultWhite){
            currentBoard.set(toBlack, oneD_pos);
        }
    }

    // implement later
    void load_customize_setup(){

    }

    auto get_all_next_boards() -> NextBoards&{

    }


    void show_current_board(){

    }


    
private:
    // functions 
    auto get_perpendicular(const pair<int, int>& direction) -> pair<pair<int, int>, pair<int, int>>& {
        int idx = 0;
        while(this->directions[idx] != direction) idx++;
        pair<pair<int, int>, pair<int, int>> perpDirections = {
            this->directions[(idx+2)%6], this->directions[(idx-2)%6]
        };
        return perpDirections;
    }

    auto get_one_piece_Next()-> NextBoards&{
        NextBoards next_boards;
        for(int oneD_pos = 0; oneD_pos < 61; oneD_pos++){
            pair<int, int> twoD_pos = mappingInverse[oneD_pos];
            if(currentBoard.is_white(oneD_pos)){
                for(int i = 0; i < 6; i++){
                    int nextPos = mapping[twoD_pos + directions[i]];
                    if(currentBoard.is_empty(nextPos)){
                        auto current_board = currentBoard.get_current_board();
                        current_board.first[nextPos] = 1;
                        current_board.first[oneD_pos] = 0;
                        next_boards.push_back(make_pair(current_board, action_id(1, i, oneD_pos)));
                    }
                }
            }
            else if(currentBoard.is_black(oneD_pos)){
                for(int i = 0; i < 6; i++){
                    int nextPos = mapping[twoD_pos + directions[i]];
                    if(currentBoard.is_empty(nextPos)){
                        auto current_board = currentBoard.get_current_board();
                        current_board.second[nextPos] = 1;
                        current_board.second[oneD_pos] = 0;
                        next_boards.push_back(make_pair(current_board, action_id(1, i, oneD_pos)));
                    }
                }
            }
        }
        return next_boards;
    }

    auto get_two_piece_Next()-> vector<pair<vector<bool>, vector<bool>>>&{
        vector<pair<vector<bool>, vector<bool>>> next_boards;
        for(int oneD_pos = 0; oneD_pos < 61; oneD_pos++){
            pair<int, int> twoD_pos = mappingInverse[oneD_pos];

        }   
    }

    auto get_three_piece_Next(){

    }

    int action_id(int num_of_piece, int directionIdx){
        if(num_of_piece == 1){
            return directionIdx;
        }
        else if(num_of_piece == 2){
            switch(directionIdx){
                
            }
        }
        else if(num_of_piece == 3){
            switch(directionIdx){

            }
        }
    }

    // data
    Board currentBoard;
    vector<pair<vector<bool>&, vector<bool>&>> allNextBoards;

    // mapping tool
    vector<pair<int, int>> directions = {
        {0, 1}, {1, 1}, {1, 0}, {0, -1}, {-1, -1}, {-1, 0}
    };
    map<pair<int, int>, int> mapping = {
        {{0, 0},  0}, {{0, 1},  1}, {{0, 2},  2}, {{0, 3},  3}, {{0, 4},  4},
        {{1, 0},  5}, {{1, 1},  6}, {{1, 2},  7}, {{1, 3},  8}, {{1, 4},  9}, {{1, 5}, 10},
        {{2, 0}, 11}, {{2, 1}, 12}, {{2, 2}, 13}, {{2, 3}, 14}, {{2, 4}, 15}, {{2, 5}, 16}, {{2, 6}, 17},
        {{3, 0}, 18}, {{3, 1}, 19}, {{3, 2}, 20}, {{3, 3}, 21}, {{3, 4}, 22}, {{3, 5}, 23}, {{3, 6}, 24}, {{3, 7}, 25},
        {{4, 0}, 26}, {{4, 1}, 27}, {{4, 2}, 28}, {{4, 3}, 29}, {{4, 4}, 30}, {{4, 5}, 31}, {{4, 6}, 32}, {{4, 7}, 33}, {{4, 8}, 34},
        {{5, 1}, 35}, {{5, 2}, 36}, {{5, 3}, 37}, {{5, 4}, 38}, {{5, 5}, 39}, {{5, 6}, 40}, {{5, 7}, 41}, {{5, 8}, 42},
        {{6, 2}, 43}, {{6, 3}, 44}, {{6, 4}, 45}, {{6, 5}, 46}, {{6, 6}, 47}, {{6, 7}, 48}, {{6, 8}, 49},
        {{7, 3}, 50}, {{7, 4}, 51}, {{7, 5}, 52}, {{7, 6}, 53}, {{7, 7}, 54}, {{7, 8}, 55},
        {{8, 4}, 56}, {{8, 5}, 57}, {{8, 6}, 58}, {{8, 7}, 59}, {{8, 8}, 60},
    };
    map<int, pair<int, int>> mappingInverse = {
        {0, {0, 0}}, {1, {0, 1}}, {2, {0, 2}}, {3, {0, 3}}, {4, {0, 4}},
        {5, {1, 0}}, {6, {1, 1}}, {7, {1, 2}}, {8, {1, 3}}, {9, {1, 4}}, {10, {1, 5}},
        {11, {2, 0}}, {12, {2, 1}}, {13, {2, 2}}, {14, {2, 3}}, {15, {2, 4}}, {16, {2, 5}}, {17, {2, 6}},
        {18, {3, 0}}, {19, {3, 1}}, {20, {3, 2}}, {21, {3, 3}}, {22, {3, 4}}, {23, {3, 5}}, {24, {3, 6}}, {25, {3, 7}},
        {26, {4, 0}}, {27, {4, 1}}, {28, {4, 2}}, {29, {4, 3}}, {30, {4, 4}}, {31, {4, 5}}, {32, {4, 6}}, {33, {4, 7}}, {34, {4, 8}},
        {35, {5, 1}}, {36, {5, 2}}, {37, {5, 3}}, {38, {5, 4}}, {39, {5, 5}}, {40, {5, 6}}, {41, {5, 7}}, {42, {5, 8}},
        {43, {6, 2}}, {44, {6, 3}}, {45, {6, 4}}, {46, {6, 5}}, {47, {6, 6}}, {48, {6, 7}}, {49, {6, 8}},
        {50, {7, 3}}, {51, {7, 4}}, {52, {7, 5}}, {53, {7, 6}}, {54, {7, 7}}, {55, {7, 8}},
        {56, {8, 4}}, {57, {8, 5}}, {58, {8, 6}}, {59, {8, 7}}, {60, {8, 8}}
    };
};