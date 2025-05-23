#include<iostream>
#include<vector>
#include<filesystem>
#include<fstream>
#include<random>
#include"AbaloneEnv.h"
#include"Board.h"
#include"Agent_minmax.h"

using namespace std;
namespace fs = std::filesystem;

fs::path relative = "../minmax_results/test.txt";
string path = (fs::current_path() / relative).string();


void run_default_game(int edge){
    AbaloneEnv game(edge);

    game.load_default_setup();

    int dep, round;
    cout << "Enter Minmax max depth:" << endl;
    cin >> dep;
    cout << "Enter Minmax round:" << endl;
    cin >> round; 
    Minimax minmax;

    minmax.start(game.currentBoard, dep, round, path);
    return;
}

void run_random_game(int edge, int pieces){
    int n, dep, round;

    cout << "Enter random state count:" << endl;
    cin >> n;
    cout << "Enter Minmax max depth:" << endl;
    cin >> dep;
    cout << "Enter Minmax round:" << endl;
    cin >> round;

    std::random_device rd;
    std::mt19937 gen(rd());

    int place = 3 * edge * (edge - 1) + 1;
    std::vector<int> v(place);
    for (int i = 0; i < place; i++) v[i] = i;

    for(int i = 0; i < n; i++){
    
        shuffle(v.begin(), v.end(), gen);

        vector<int> A(v.begin(), v.begin() + pieces);
        vector<int> B(v.begin() + pieces, v.begin() + 2*pieces);

        AbaloneEnv game(edge);
        game.load_customize_setup(A, B);

        Minimax minmax;

        minmax.start(game.currentBoard, dep, round, path);
    }
}


int main(){
    //run_default_game(5);
    run_random_game(5, 14);
}