#include <iostream>
#include <vector>
#include <map>
#include "Board.h"
#pragma once
#define NextBoards vector<pair<Board,int>>

using namespace std;

class AbaloneAction{
    public:
    int numberofpiece;
    int oneDpos;
    /**
     * one piece
     * first :[0, 5]
     * second :0
     * two and three pieces
     * first :[0, 5] the direction of otherpiece
     * second :[-1,1]
     */
    pair<int, int> direction;
    /**
     * @brief type of action according to number of piece and second direction
     * 
     * `0`: 1 piece
     * 
     * `1`: 2 pieces ,sec_dir = -1
     * 
     * `2`: 2 pieces ,sec_dir = 0
     * 
     * `3`: 2 pieces ,sec_dir = 1
     * 
     * `4`: 3 pieces ,sec_dir = -1
     * 
     * `5`: 3 pieces ,sec_dir = 0
     * 
     * `6`: 3 pieces ,sec_dir = 1
    */
    int type = 0;
    AbaloneAction(){}
    void set_type();
    void load_type();
    int value();
    void load_value(int value);
};


pair<int, int> operator+ (pair<int, int>& pos1, pair<int, int>& pos2);



class AbaloneEnv
{
public:
    AbaloneEnv();

    AbaloneEnv(int n);

    AbaloneEnv(Board board);

    void load_board(Board board);

    void load_default_setup();

    // implement later
    void load_customize_setup(vector<int> white_setup, vector<int> black_setup);

    auto get_all_next_boards() -> NextBoards;

    void show_current_board();

    vector<pair<int, int>> oneD_to_twoD;

    // functions

    void get_one_piece_Next(NextBoards& candidate);

    void get_two_piece_Next(NextBoards& candidate);

    void get_three_piece_Next(NextBoards& candidate);

    int distance_to_center(pair<int, int>& position);

    /**
     * @brief Player color flag.
     * 
     * `false`  :player is white
     * 
     * `true` :player is black
     */
    int population(bool player);

    void visit_population(pair<int, int> position, vector<vector<bool>>& visited, bool player);

    bool is_empty(pair<int, int>& position);
    bool is_white(pair<int, int>& position);
    bool is_black(pair<int, int>& position);
    bool is_ally(pair<int, int>& position);
    bool is_enemy(pair<int, int>& position);
    bool is_valid(pair<int, int> position);

    int count_neighbors(pair<int, int> pos, bool is_white);
    bool can_push(int idx);
    int distance_to_edge(pair<int,int> pos); 

    // data
    int number_of_edge, number_of_place;

    Board currentBoard;
    // mapping tool
    vector<pair<int, int>> directions;
    
    int twoD_to_oneD(pair<int, int> position);
    int count;
    
};