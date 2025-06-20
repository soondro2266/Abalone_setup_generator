#include <vector>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <limits> 
#include <string>
#include <cmath>
#include "AbaloneEnv.h"
#include "Agent_minmax.h"
#include "Board.h"
#define MIN std::numeric_limits<long double>::lowest()
#define MAX std::numeric_limits<long double>::max()


using namespace std;



void Minimax::start(Board initial_state, int max_depth, int max_round, string path){
    vector<pair<Board, int>> best_moves;


    AbaloneEnv game = AbaloneEnv(initial_state);
    this->max_depth = max_depth;

    for(int round = 0; round < max_round; round++){
        game.count++;
        pair<Board, int> best_move = find_best_action(game);
        best_moves.push_back(best_move);
        game.load_board(best_move.first);
        game.show_current_board();
    }

    std::ofstream file(path);
    for(auto best_move : best_moves){
        for(int oneDpos = 0; oneDpos < game.number_of_place; oneDpos++){
            file << best_move.first.white[oneDpos] + 2 * best_move.first.black[oneDpos];
        }
        file << " ";
        file << best_move.second << endl;
    }
    file.close();
    return;
}

pair<Board, int> Minimax::find_best_action(AbaloneEnv& game){
    pair<Board, int> best_move;
    vector<pair<Board, int>> all_moves = game.get_all_next_boards();
    if(!game.currentBoard.player){ // white move first
        long double max_eval = MIN;
        for(auto move : all_moves){
            long double eval = alphabeta(move.first, 1, !game.currentBoard.player, MIN, MAX);
            if(eval > max_eval){
                max_eval = eval;
                best_move = move;
            }
        }
    }
    else{
        long double min_eval = MAX;
        for(auto move : all_moves){
            long double eval = alphabeta(move.first, 1, !game.currentBoard.player, MIN, MAX);
            if(eval < min_eval){
                min_eval = eval;
                best_move = move;
            }
        }
    }
    return best_move;
}


long double Minimax::alphabeta(Board& current_state, int depth, bool maximizingPlayer, long double alpha, long double beta) {

    AbaloneEnv current_game = AbaloneEnv(current_state);

    if (depth == max_depth || current_state.black_piece <= 8 || current_state.white_piece <= 8) {
        long double result = heuristic(current_game);
        //current_game.show_current_board();
        //cout << result << endl;
        return result;
    }
    vector<pair<Board, int>> all_next_move = current_game.get_all_next_boards();
    pair<Board, int> best_move;

    

    if (!maximizingPlayer) {
        long double maxEval = MIN;      
        for (auto next_move : all_next_move) {
            long double eval = alphabeta(next_move.first , depth + 1, !maximizingPlayer, alpha, beta);
            if(eval > maxEval){
                best_move = next_move;
                maxEval = eval;
            }
            
            alpha = max(alpha, eval);

            if (beta <= alpha)
                break;  // Beta cut-off
        }

        return maxEval;
    }
    else {
        long double minEval = MAX;

        for (auto next_move : all_next_move) {
            long double eval = alphabeta(next_move.first, depth + 1, !maximizingPlayer, alpha, beta);
            if(eval < minEval){
                minEval = eval;
                best_move = next_move;
            }
            beta = min(beta, eval);

            if (beta <= alpha)
                break;  // Alpha cut-off
        }

        return minEval;
    }
}

long double Minimax::heuristic(AbaloneEnv& state){

    int pieces_of_white = 0;
    int pieces_of_black = 0;
    int score = 0;
    for(int oneDpos = 0; oneDpos < state.number_of_place; oneDpos++){
        pair<int, int> position = state.oneD_to_twoD[oneDpos];
        if(state.currentBoard.white[oneDpos]){
            pieces_of_white++;
            switch (state.distance_to_center(position))
            {
            case 4:
                score += 500;
                break;
            case 3:
                score += 100;
                break;
            case 2:
                score -= 0;
                break;
            case 1:
                score -= 200;
                break;
            case 0:
                score -= 300;
                break;
            }
            
        }
        if(state.currentBoard.black[oneDpos]){
            int dis = state.distance_to_center(position);
            pieces_of_black++;
            switch (state.distance_to_center(position))
            {
            case 4:
                score -= 500;
                break;
            case 3:
                score -= 100;
                break;
            case 2:
                score += 0;
                break;
            case 1:
                score += 200;
                break;
            case 0:
                score += 300;
                break;
            }
        }
    }
    score /= pow(state.count, 2);
    score -= 300*(state.population(true) - state.population(false));
    score -= 30000*(pieces_of_white - pieces_of_black);
    
    return score;
}

