#include <vector>
#include <iostream>
#include <algorithm>
#include <string>
using namespace std;

/*
class Tree
{
public:
	int depth;
	
	Minimax* parent_node; //應該是只有一個parent node
	Tree(int depth, vector<bool> initial_white_state, vector<bool> initial_black_state);
	Tree();
	~Tree();

};
*/


class Minimax
{
public:
	int depth;
	vector<bool> white_state;
	vector<bool> black_state;
	vector<string> action;

	Minimax(int depth, vector<bool> white_state, vector<bool> black_state);
	Minimax();
	~Minimax();

	int heuristic(vector<bool> white_state, vector<bool> black_state, int depth);
	int alphabeta(vector<bool> white_state, vector<bool> black_state, int depth, bool maximizingPlayer, int alpha, int beta);
};

