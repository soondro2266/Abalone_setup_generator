#include <vector>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <limits> 
#include <string>
#include <cmath>
#include "AbaloneEnv.h"
#include "Board.h"
#pragma once

using namespace std;

/**
 * @brief The alpha-beta agent decide which step to move, and save the action data 
 * for behavior cloning to train CNN.  
 */
class Minimax
{
    public:

    /**
     * @brief constructor
     */
    Minimax(){}

    /**
     * @brief call start to play game with the given board
     *  
     * best_moves record the action it take 
     * 
     * @param max_round how many times to play, each time call alpha-beta function to decide which steps to take
     */
    void start(Board initial_state, int max_depth, int max_round, string path = "minmax_result.txt");

    /**
     * @brief call all possible action recusively 
     * @return when depth == max_depth or the game is over
     */
    long double alphabeta(Board& current_state, int depth, bool maximizingPlayer, long double alpha, long double beta);
    
    /**
     * @brief call alpha-beta function get all possible actions score, and return the action with highest score
     * @return best_move is a pair<Board, correspond best action>
     */
    pair<Board, int> find_best_action(AbaloneEnv& game);
    
    /**
     * @brief run through entire board, count the number of white 、 black and the distance to center 
     * 
     * score the more closer to center, the more higher score add for white, black is vice versa and the affect of distance will decrease by divide pow(count of steps, 2)
     * 
     * score added if they are more closer by count population the smaller the better
     * 
     * score added if the number of chess is more than component, give a large score
     * 
     * @return score compute by heuristic 
     */
    long double heuristic(AbaloneEnv& state);

private:
    int max_depth;
};