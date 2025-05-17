#include <iostream>
#include <vector>
#include <map>
#include "Board.h"
#include "AbaloneEnv.h"
#define toWhite 1
#define toBlack 2
#define toEmpty 3
#define NextBoards vector<pair<Board,int>>

using namespace std;

pair<int, int> operator+ (pair<int, int>& pos1, pair<int, int>& pos2){
    return make_pair(pos1.first + pos2.first, pos1.second + pos2.second);
}

void AbaloneAction::set_type(){
    type = 0;
    if(numberofpiece != 1){
        type = 3 * numberofpiece - 4 + direction.second;
    }
}
void AbaloneAction::load_type(){
    switch (type)
    {
    case 0:
        numberofpiece = 0;
        direction.second = 0;
        break;
    case 1:
        numberofpiece = 2;
        direction.second = -1;
        break;
    case 2:
        numberofpiece = 2;
        direction.second = 0;
        break;
    case 3:
        numberofpiece = 2;
        direction.second = 1;
        break;
    case 4:
        numberofpiece = 3;
        direction.second = -1;
        break;
    case 5:
        numberofpiece = 3;
        direction.second = 0;
        break;
    case 6:
        numberofpiece = 3;
        direction.second = 1;
        break;
    }
    return;
}
int AbaloneAction::value(){
    set_type();
    return oneDpos*42+type*6+direction.first;
}
void AbaloneAction::load_value(int value){
    oneDpos = value/42;
    value %= 42;
    type = value/6;
    direction.first = value%6;
    load_type();
    return;
}

AbaloneEnv::AbaloneEnv(){}

AbaloneEnv::AbaloneEnv(int n){
    number_of_edge = n;
    currentBoard = Board(n);
    number_of_place = 3 * n * (n - 1) + 1;
    directions = {{0, 1}, {1, 1}, {1, 0}, {0, -1}, {-1, -1}, {-1, 0}};
    //consturct oneD-to-twoD
    for(int i = 0; i < 2*n-1; i++){
        for(int j = 0; j < 2*n-1; j++){
            pair<int, int> position = make_pair(i, j);
            if(is_valid(position)){
                oneD_to_twoD.push_back(position);
            }
        }
    }
}

AbaloneEnv::AbaloneEnv(Board board){
    currentBoard = board;
    int n = board.n;
    number_of_edge = n;
    number_of_place = 3 * n * (n - 1) + 1;
    directions = {{0, 1}, {1, 1}, {1, 0}, {0, -1}, {-1, -1}, {-1, 0}};
    int cnt = 0;
    //consturct oneD-to-twoD
    for(int i = 0; i < 2*n-1; i++){
        for(int j = 0; j < 2*n-1; j++){
            pair<int, int> position = make_pair(i, j);
            if(is_valid(position)){
                oneD_to_twoD.push_back(position);
            }
        }
    }
}

void AbaloneEnv::load_board(Board board){
    currentBoard = board;
}

void AbaloneEnv::load_default_setup(){
    vector<int> defaultWhite = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15};
    vector<int> defaultBlack = {56, 57, 58, 50, 51, 52, 53, 54, 55, 45, 46, 47, 59, 60};
    currentBoard = Board(number_of_edge);
    for(int oneDpos : defaultWhite){
        currentBoard.set(1, oneD_to_twoD[oneDpos].first, oneD_to_twoD[oneDpos].second);
    }
    for(int oneDpos : defaultBlack){
        currentBoard.set(2, oneD_to_twoD[oneDpos].first, oneD_to_twoD[oneDpos].second);
    }
    currentBoard.white_piece = defaultWhite.size();
    currentBoard.black_piece = defaultBlack.size();
}


void AbaloneEnv::load_customize_setup(){

}

auto AbaloneEnv::get_all_next_boards() -> NextBoards{
    NextBoards candidate;
    get_one_piece_Next(candidate);
    get_two_piece_Next(candidate);
    get_three_piece_Next(candidate);
    return candidate;
}


void AbaloneEnv::show_current_board(){
    vector<vector<int>> mask = vector(2 * number_of_edge - 1,vector(4 * number_of_edge - 1, 0));
    for(int i = 0; i < 2*number_of_edge - 1; i++){
        for(int j = 0; j < 2*number_of_edge - 1; j++){
            pair<int, int> position = make_pair(i, j);
            if(!is_valid(position))continue;
            int mask_j;
            if(i < number_of_edge){
                mask_j = abs(number_of_edge - i - 1) + 2 * j;
            }
            else{
                mask_j = abs(number_of_edge - i - 1) + 2 * (j - i + number_of_edge - 1);
            }
            if(is_white(position)){
                mask[i][mask_j] = 1;
            }
            else if(is_black(position)){
                mask[i][mask_j] = 2;
            }
            else{
                mask[i][mask_j] = 3;
            }
        }
    }
    for(int i = 0; i < 2 * number_of_edge - 1; i++){
        for(int j = 0; j < 4 * number_of_edge - 1; j++){
            if(mask[i][j] == 1){
                cout << "W";
            }
            else if(mask[i][j] == 2){
                cout << "B";
            }
            else if(mask[i][j] == 3){
                cout << ".";
            }
            else{
                cout << " ";
            }
        }
        cout << endl;
    }
}


void AbaloneEnv::get_one_piece_Next(NextBoards& candidate){
    AbaloneAction action;
    action.numberofpiece = 1;
    action.direction.second = 0;
    for(int oneD_pos = 0; oneD_pos < number_of_place; oneD_pos++){
        pair<int, int> position = oneD_to_twoD[oneD_pos];
        if(!is_ally(position)) continue;
        action.oneDpos = oneD_pos;
        for(int direction = 0; direction < 6; direction++){
            action.direction.first = direction;
            pair<int, int> nextPos = position + directions[direction];
            if(is_empty(nextPos)){
                Board nextBoard = currentBoard;
                nextBoard.set_empty(position);
                nextBoard.set_ally(nextPos);
                nextBoard.player = !(nextBoard.player);
                candidate.push_back(make_pair((nextBoard), action.value()));
            }
        }
    }
    return;
}

void AbaloneEnv::get_two_piece_Next(NextBoards& candidate){
    AbaloneAction action;
    action.numberofpiece = 2;
    for(int oneD_pos = 0; oneD_pos < number_of_place; oneD_pos++){
        pair<int, int> position = oneD_to_twoD[oneD_pos];
        if(!is_ally(position)) continue;
        action.oneDpos = oneD_pos;
        for(int direction = 0; direction < 6; direction++){
            pair<int, int> position2 = position + directions[direction];
            if(!is_ally(position2)) continue;
            action.direction.first = direction;
            for(int second_direction = -1; second_direction <= 1; second_direction++){
                action.direction.second = second_direction;
                if(second_direction == 0){ //regular push
                    pair<int, int> target = position2 + directions[direction];
                    if(is_empty(target)){ // no enemy
                        Board nextBoard = currentBoard;
                        nextBoard.set_empty(position);
                        nextBoard.set_ally(target);
                        nextBoard.player = !(nextBoard.player);
                        candidate.push_back(make_pair(nextBoard, action.value()));
                    }
                    else if(is_enemy(target)){ //2 push 1
                        pair<int, int> target2 = target + directions[direction];
                        if(is_empty(target2)){ //push to empty
                            Board nextBoard = currentBoard;
                            nextBoard.set_empty(position);
                            nextBoard.set_ally(target);
                            nextBoard.set_enemy(target2);
                            nextBoard.player = !(nextBoard.player);
                            candidate.push_back(make_pair(nextBoard, action.value()));
                        }
                        else if(!is_valid(target2)){ //push to void
                            Board nextBoard = currentBoard;
                            nextBoard.set_empty(position);
                            nextBoard.set_ally(target);
                            nextBoard.remove_enemy();
                            nextBoard.player = !(nextBoard.player);
                            candidate.push_back(make_pair(nextBoard, action.value()));
                        }
                    }
                }
                else{//side move
                    int move_direction = (direction + second_direction + 6) % 6;
                    //cout << move_direction << "\n";
                    pair<int, int> target1 = position + directions[move_direction];
                    pair<int, int> target2 = position2 + directions[move_direction];
                    if(!(is_empty(target1) && is_empty(target2))) continue;
                    Board nextBoard = currentBoard;
                    nextBoard.set_empty(position);
                    nextBoard.set_empty(position2);
                    nextBoard.set_ally(target1);
                    nextBoard.set_ally(target2);
                    nextBoard.player = !(nextBoard.player);
                    candidate.push_back(make_pair(nextBoard, action.value()));
                }
            }
        }
    }
    return;
}

void AbaloneEnv::get_three_piece_Next(NextBoards& candidate){
    AbaloneAction action;
    action.numberofpiece = 3;
    for(int oneD_pos = 0; oneD_pos < number_of_place; oneD_pos++){
        pair<int, int> position = oneD_to_twoD[oneD_pos];
        if(!is_ally(position)) continue;
        action.oneDpos = oneD_pos;
        for(int direction = 0; direction < 6; direction++){
            pair<int, int> position2 = position + directions[direction];
            if(!is_ally(position2)) continue;
            pair<int, int> position3 = position2 + directions[direction];
            if(!is_ally(position3)) continue;
            action.direction.first = direction;
            for(int second_direction = -1; second_direction <= 1; second_direction++){
                action.direction.second = second_direction;
                if(second_direction == 0){ //regular push
                    pair<int, int> target = position3 + directions[direction];
                    if(is_empty(target)){ // no enemy
                        Board nextBoard = currentBoard;
                        nextBoard.set_empty(position);
                        nextBoard.set_ally(target);
                        nextBoard.player = !(nextBoard.player);
                        candidate.push_back(make_pair(nextBoard, action.value()));
                    }
                    else if(is_enemy(target)){
                        pair<int, int> target2 = target + directions[direction];
                        if(is_empty(target2)){ //3 push 1 to empty
                            Board nextBoard = currentBoard;
                            nextBoard.set_empty(position);
                            nextBoard.set_ally(target);
                            nextBoard.set_enemy(target2);
                            nextBoard.player = !(nextBoard.player);
                            candidate.push_back(make_pair(nextBoard, action.value()));
                        }
                        else if(!is_valid(target2)){ //3 push 1 to void
                            Board nextBoard = currentBoard;
                            nextBoard.set_empty(position);
                            nextBoard.set_ally(target);
                            nextBoard.remove_enemy();
                            nextBoard.player = !(nextBoard.player);
                            candidate.push_back(make_pair(nextBoard, action.value()));
                        }
                        else if(is_enemy(target2)){
                            pair<int, int> target3 = target2 + directions[direction];
                            if(is_empty(target3)){ //3 push 2 to empty
                                Board nextBoard = currentBoard;
                                nextBoard.set_empty(position);
                                nextBoard.set_ally(target);
                                nextBoard.set_enemy(target3);
                                nextBoard.player = !(nextBoard.player);
                                candidate.push_back(make_pair(nextBoard, action.value()));
                            }
                            else if(!is_valid(target3)){ // 3 push 2 to void
                                Board nextBoard = currentBoard;
                                nextBoard.set_empty(position);
                                nextBoard.set_ally(target);
                                nextBoard.remove_enemy();
                                nextBoard.player = !(nextBoard.player);
                                candidate.push_back(make_pair(nextBoard, action.value()));
                            }
                        }
                    }
                }
                else{//side move
                    int move_direction = (direction + second_direction + 6) % 6;
                    pair<int, int> target1 = position + directions[move_direction];
                    pair<int, int> target2 = position2 + directions[move_direction];
                    pair<int, int> target3 = position3 + directions[move_direction];
                    if(!(is_empty(target1) && is_empty(target2) && is_empty(target3))) continue;
                    Board nextBoard = currentBoard;
                    nextBoard.set_empty(position);
                    nextBoard.set_empty(position2);
                    nextBoard.set_empty(position3);
                    nextBoard.set_ally(target1);
                    nextBoard.set_ally(target2);
                    nextBoard.set_ally(target3);
                    nextBoard.player = !(nextBoard.player);
                    candidate.push_back(make_pair(nextBoard, action.value()));
                }
            }
        }
    }
    return;
}

bool AbaloneEnv::is_empty(pair<int, int>& position){
    if(!is_valid(position))return false;
    auto result = currentBoard.get(position.first, position.second);
    return result.first == 0 && result.second == 0;
}
bool AbaloneEnv::is_white(pair<int, int>& position){
    if(!is_valid(position))return false;
    auto result = currentBoard.get(position.first, position.second);
    return result.first == 1;
}
bool AbaloneEnv::is_black(pair<int, int>& position){
    if(!is_valid(position))return false;
    auto result = currentBoard.get(position.first, position.second);
    return result.second == 1;
}
bool AbaloneEnv::is_ally(pair<int, int>& position){
    return currentBoard.player ? is_black(position) : is_white(position);
}
bool AbaloneEnv::is_enemy(pair<int, int>& position){
    return currentBoard.player ? is_white(position) : is_black(position);
}
bool AbaloneEnv::is_valid(pair<int, int> position){
    if(position.first  < 0 || 
        position.second < 0 ||
        position.first  >= 2 * number_of_edge - 1 ||
        position.second >= 2 * number_of_edge - 1 ||
        position.first - position.second >=  number_of_edge ||
        position.first - position.second <= -number_of_edge){
        return false;
    }
    return true;
}

int AbaloneEnv::distance_to_center(pair<int, int>& position){
    int y = position.first-position.second;
    return max(abs(position.first - number_of_edge + 1),max(abs(y), abs(position.second - number_of_edge + 1)));
}

int AbaloneEnv::population(bool player){
    vector<vector<bool>> visited = vector(2*number_of_edge-1, vector(2*number_of_edge-1, false));
    int result = 0;
    if(!player){
        for(int oneDpos = 0; oneDpos < number_of_place; oneDpos++){
            pair<int, int> position = oneD_to_twoD[oneDpos];
            if(currentBoard.white[oneDpos] == 1 && !visited[position.first][position.second]){
                visit_population(position, visited, player);
                result++;
            }
        }
    }
    else{
        for(int oneDpos = 0; oneDpos < number_of_place; oneDpos++){
            pair<int, int> position = oneD_to_twoD[oneDpos];
            if(currentBoard.black[oneDpos] == 1 && !visited[position.first][position.second]){
                visit_population(position, visited, player);
                result++;
            }
        }
    }
    return result;
}

void AbaloneEnv::visit_population(pair<int, int> position, vector<vector<bool>>& visited, bool player){
    visited[position.first][position.second] = true;
    for(int direction = 0; direction < 6; direction++){
        pair<int, int>neighbor = position + directions[direction];
        if(!player){
            if(is_white(neighbor) && !visited[neighbor.first][neighbor.second]){
                visit_population(neighbor, visited, player);
            }
        }
        else{
            if(is_black(neighbor) && !visited[neighbor.first][neighbor.second]){
                visit_population(neighbor, visited, player);
            }
        }
    }
    return;
}

int AbaloneEnv::twoD_to_oneD(pair<int, int> position){
    int result;
    int n = number_of_edge;
    int i = position.first;
    int j = position.second;
    if(i < n){
        result = i*(2*n + i - 1)/2 + j;
    }
    else{
        result = 3*n*i - i*(i+5)/2 - n*(n-2) + j - 1;
    }
    return result;
}