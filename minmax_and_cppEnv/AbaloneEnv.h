#include <iostream>
#include <vector>
#include <map>
#include "Board.h"
#pragma once
#define NextBoards vector<pair<Board,int>>

using namespace std;

/**
 * ### AbaloneAction
 * The action on the Abalone
 */
class AbaloneAction{
    public:
    /**
     * @brief How many pieces move together
     */
    int numberofpiece;
    /**
     * @brief One-dimenson position of the first piece
     */
    int oneDpos;
    /**
     * @brief Direction of movement
     * 
     * `first`: Direction of first piece to other pieces
     * 
     * (The movement of one pieces)
     * 
     * [0, 5] 
     * 
     * `second`: The gap between movement direction and align direction
     * 
     * [-1, 1]
     */
    pair<int, int> direction;
    /**
     * @brief Type of action
     * 
     * According to number of piece and second direction
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
    /**
     * default constructor
     */
    AbaloneAction(){}
    /**
     * @brief Set the type
     * 
     * Use the number of pieces and second direction to set the type
     */
    void set_type();
    /**
     * @brief Load the type
     * 
     * Use the type to set the second direction and number of pieces
     */
    void load_type();
    /**
     * @brief #### Get the action value
     * 
     * One action has one unique action value
     * 
     * Consider a 3-D array 
     * 
     * `first Dimension`: oneDpos
     * 
     * `second Dimension`: type
     * 
     * `third Dimension`: first direction
     *
     * The action value is the index of this action on this array
     * 
     * (after flatten)
     */
    int value();
    /**
     * @brief use value to set up action
     */
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
     * @brief initialize AbaloneEnv with edge = n
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
     * @brief setting board with designated position of white、black piece
     */
    void load_customize_setup(vector<int> white_setup, vector<int> black_setup);

    /**
     * @brief print the entire board, if the position is white then cout "W" in the position, if is black cout "B", if empty cout "."
     */
    void show_current_board();

    /**
     * @brief look for all possible move for only moving one piece
     * @param candidate record all possible moves
     */
    void get_one_piece_Next(NextBoards& candidate);

    /**
     * @brief look for all possible move for moving exactly two pieces
     * @param candidate record all possible moves
     */
    void get_two_piece_Next(NextBoards& candidate);

    /**
     * @brief look for all possible move for moving exactly three pieces
     * @param candidate record all possible moves
     */
    void get_three_piece_Next(NextBoards& candidate);

    /**
     * @brief called by population to implement dfs recusively
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