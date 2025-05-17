#include<iostream>
#include<vector>
#include"AbaloneEnv.h"
#include"Board.h"
#include"Agent_minmax.h"

using namespace std;

int main(){

    AbaloneEnv game(5);

    game.load_default_setup();

    int dep, round;
    cout << "Enter Minmax max depth:" << endl;
    cin >> dep;
    cout << "Enter Minmax round:" << endl;
    cin >> round; 
    Minimax minmax;

    minmax.start(game.currentBoard, dep, round);
}