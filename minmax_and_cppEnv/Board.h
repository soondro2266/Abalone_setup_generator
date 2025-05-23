#include<iostream>
#include<vector>
#pragma once
using namespace std;

class Board
{
public:
    /**
     * @brief Player color flag.
     * 
     * `false`  :player is white
     * 
     * `true` :player is black
     */
    bool player;
    Board();
    /**
    * @brief Constructs a Board of given size, initializing all positions to empty.
    *
    * Initializes two boolean vectors, `white` and `black`, each of length
    * 61 (sufficient for a standard Abalone board layout), with all entries set to false.
    *
    * @param size The dimension parameter `n` determining the board layout.
    */
    Board(int size);
    /**
    * Return the occupancy state at board position (x, y).
    *
    *
    * @param x The row coordinate (0-based).
    * @param y The column coordinate (0-based).
    * @return A `pair<bool,bool>`
    * first  = white,   second = black
    */
    pair<bool, bool> get(int x, int y);
    /**
    * Sets the board position (x, y) to the given state by converting it into a 1D index.
    *
    * @param state The desired state: 1 = white piece, 2 = black piece, 3 = empty
    * @param x     The row coordinate (0-based)
    * @param y     The column coordinate (0-based)
    */
    void set(int state, int x, int y);
    void set_ally(pair<int, int>& position);
    void set_enemy(pair<int, int>& position);
    void set_empty(pair<int, int>& position);
    void remove_enemy();
    int n;
    int white_piece;
    int black_piece;
    vector<bool> white;
    vector<bool> black;
};