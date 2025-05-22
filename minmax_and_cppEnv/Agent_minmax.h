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


class Minimax
{
    public:
    Minimax(){}

    Minimax(int n);

    void start(Board initial_state, int max_depth, int max_round, string path = "minmax_result.txt");


    long double alphabeta(Board& current_state, int depth, bool maximizingPlayer, long double alpha, long double beta);

    pair<Board, int> find_best_action(AbaloneEnv& game);
    
    long double heuristic(AbaloneEnv& state);

private:
    int max_depth;
};