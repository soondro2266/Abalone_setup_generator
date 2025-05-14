#include "Agent_minmax.h"
#include <vector>
#include <algorithm> // for max, min
#include <climits>   // for INT_MIN, INT_MAX

using namespace std;
/*
Tree::Tree(int depth, vector<bool> initial_white_state, vector<bool> initial_black_state) {
	this->depth = depth;	//總深度，可能不會用到
	this->parent_node = new Minimax(depth, initial_white_state, initial_black_state);		//初始化parent minimax node
	
}

Tree::~Tree() {

}
*/

Minimax::Minimax(int depth, vector<bool> white_state, vector<bool> black_state) {
	this->depth = depth;
	this->white_state = white_state;
	this->black_state = black_state;	
}

int Minimax::alphabeta(vector<bool> white_state, vector<bool> black_state, int depth, bool maximizingPlayer, int alpha, int beta) {

    if (depth == 0 /* || isTerminal(white_state, black_state) */) {
        return heuristic(white_state, black_state, depth);
    }

    if (maximizingPlayer) {
        int maxEval = INT_MIN;
        vector<vector<bool>> possible_white_moves = /*generateMoves(white_state)*/;

        for (const auto& new_white_state : possible_white_moves) {
            int eval = alphabeta(new_white_state, black_state, depth - 1, !maximizingPlayer, alpha, beta);
            maxEval = max(maxEval, eval);
            alpha = max(alpha, eval);

            if (beta <= alpha)
                break;  // Beta cut-off
        }

        return maxEval;
    }
    else {
        int minEval = INT_MAX;

        // TODO: Generate all possible black moves
        vector<vector<bool>> possible_black_moves = /*generateMoves(black_state)*/;

        for (const auto& new_black_state : possible_black_moves) {
            int eval = alphabeta(white_state, new_black_state, depth - 1, true, alpha, beta);
            minEval = min(minEval, eval);
            beta = min(beta, eval);

            if (beta <= alpha)
                break;  // Alpha cut-off
        }

        return minEval;
    }
}

int Minimax::heuristic(vector<bool> white_state, vector<bool> black_state, int depth) {

}


