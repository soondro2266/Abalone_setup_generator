#include<iostream>
#include<vector>
#include"Board.h"

using namespace std;

Board::Board(){
    n = 5;
    white = vector<bool>(61, 1);
}

Board::Board(int size){
    n = size;
    white = vector<bool>(61, 0);
    black = vector<bool>(61, 0);
    player = 0;
}
pair<bool, bool> Board::get(int x, int y){
    int idx = 0;
    if(x < n){
        idx = x*(2*n + x - 1)/2 + y;
    }
    else{
        idx = 3*n*x - x*(x+5)/2 - n*(n-2) + y - 1;
    }
    return make_pair(white[idx], black[idx]);
}
void Board::set(int state, int x, int y){
    int idx = 0;
    if(x < n){
        idx = x*(2*n + x - 1)/2 + y;
    }
    else{
        idx = 3*n*x - x*(x+5)/2 - n*(n-2) + y - 1;
    }
    switch(state){
        case 1:
            white[idx] = 1;
            black[idx] = 0;
            break;
        case 2:
            white[idx] = 0;
            black[idx] = 1;
            break;
        case 3:
            white[idx] = 0;
            black[idx] = 0;
            break;
    }
}
void Board::set_ally(pair<int, int>& position){
    set(1 + player, position.first, position.second);
}
void Board::set_enemy(pair<int, int>& position){
    set(1 + !player, position.first, position.second);
}
void Board::set_empty(pair<int, int>& position){
    set(3, position.first, position.second);
}

void Board::remove_enemy(){
    if(!player){
        black_piece--;
    }
    else{
        white_piece--;
    }
}
