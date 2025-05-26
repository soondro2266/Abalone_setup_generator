#include <iostream>
#include <vector>
#include <map>
#include "Board.h"
#pragma once
#define NextBoards vector<pair<Board,int>>

using namespace std;

/**
 * 
 */
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


/**
 * @brief Abalone game enviorment
 * 
 * `false`  :player is white
 * 
 * `true` :player is black
 */
class AbaloneEnv
{
public:
    /**
     * default constructor
     */
    AbaloneEnv(){};

    /**
     * @brief initialize AbaloneEnv with edge = n，set currentBoard = new board
     */
    AbaloneEnv(int n);

    /**
     * @brief initialize AbaloneEnv with edge = board's edge
     * @param board currentBoard set equal to board 
     */
    AbaloneEnv(Board board);

    /**
     * @brief update currentBoard
     * @param board set currentBoard = new board
     */
    void load_board(Board board);

    /**
     * @brief setting board to default setting
     */
    void load_default_setup();

    /**
     * @brief setting board with designated position of white、black chess 
     */
    void load_customize_setup(vector<int> white_setup, vector<int> black_setup);

    /**
     * @brief print the entire board, if the position is white then cout "W" in the position, if is black cout "B", if empty cout "."
     */
    void show_current_board();

    /**
     * @brief look for all possible move for only moving one chess
     * @param candidate record all possible moves
     */
    void get_one_piece_Next(NextBoards& candidate);

    /**
     * @brief look for all possible move for moving exactly two chess
     * @param candidate record all possible moves
     */
    void get_two_piece_Next(NextBoards& candidate);

    /**
     * @brief look for all possible move for moving exactly three chess
     * @param candidate record all possible moves
     */
    void get_three_piece_Next(NextBoards& candidate);

    /**
     * @brief called by population to implement bfs recusively
     */
    void visit_population(pair<int, int> position, vector<vector<bool>>& visited, bool player);
    
    /**
     * @brief check is empty
     * @return true if the coordinate is (0,0) represent empty
     */
    bool is_empty(pair<int, int>& position);

    /**
     * @brief check is white
     * @return true if the coordinate is (1,0) represent white
     */
    bool is_white(pair<int, int>& position);

    /**
     * @brief check is black
     * @return true if the coordinate is (0,1) represent black
     */
    bool is_black(pair<int, int>& position);

    /**
     * @brief check if it can push opponent chess
     */
    bool can_push(int idx);

    /**
     * @brief check whether the position's chess is ally(same color)
     */
    bool is_ally(pair<int, int>& position);

    /**
     * @brief check whether the position's chess is enemy(different color)
     */
    bool is_enemy(pair<int, int>& position);

    /**
     * @brief check is the position is valid to put chess 
     */
    bool is_valid(pair<int, int> position);

    /**
     * @brief call function get_one、two、three_piece_Next to get all possible move in current borad
     * @return candidate which save all possible move
     */
    auto get_all_next_boards() -> NextBoards;

    /**
     * @brief save 6 valid direction chess can move
     */
    vector<pair<int, int>> directions;

    /**
     * @brief store two dimensional position of chess
     */
    vector<pair<int, int>> oneD_to_twoD;

    /**
     * @brief count of steps
     */
    int count;

    /**
     * @brief turn coordinate from two dimension to one dimension
     */
    int twoD_to_oneD(pair<int, int> position);

    /**
     * @brief count neighbor in six direcion
     */
    int count_neighbors(pair<int, int> pos, bool is_white);

    /**
     * @brief distance to closet edge
     */
    int distance_to_edge(pair<int,int> pos); 

    /**
     * @brief distance to center
     */
    int distance_to_center(pair<int, int>& position);

    /**
     * @brief use bfs to count groups of white or black 
     * @param player is white or black
     * @return the number of group
     */
    int population(bool player);

    int number_of_edge;
    int number_of_place;
    Board currentBoard;
    
};