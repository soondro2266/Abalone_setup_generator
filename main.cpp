#include<iostream>
#include<vector>
#include"AbaloneEnv.h"
#include"Board.h"

using namespace std;

int main(){

    AbaloneEnv game(5);
    game.load_default_setup();

    vector<pair<Board, int>> all_move;

    all_move = game.get_all_next_boards();

    for(auto fddffd: all_move){
        AbaloneEnv aaa(fddffd.first);
        aaa.show_current_board();
        cout << endl;
    }
}