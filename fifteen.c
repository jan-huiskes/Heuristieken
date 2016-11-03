/******************************************************************************
    * fifteen.c
    *
    * Computer Science 50
    * Problem Set 3
    *
    * Implements Game of Fifteen (generalized to d x d).
    *
    * Usage: fifteen d
    *
    * whereby the board's dimensions are to be d x d,
    * where d must be in [DIM_MIN,DIM_MAX]
    *
    * Note that usleep is obsolete, but it offers more granularity than
    * sleep and is simpler to use than nanosleep; `man usleep` for more.
    * 
    * Edited by:
    * Name: Boris Wolvers
    * Student number: 10801936
    * Date: 23-9-2016
    * Filename: fifteen.c
    * Assignment: Hacker fifteen
    * 
    * Description: The task for the student (me) is to complete the code
    * for the game of fifteen by filling in the next functions: init(), 
    * draw(), move() and won(). Furthermore I have to implement God Mode, 
    * an algorithm which solves the game. I have used a recursive approach,
    * I think it's called iterative deepening.
    *
    * Furthermore, in some cases the God-mode function does take quite long
    * to solve the puzzle, however, I know for certain GOD-Mode will solve
    * the puzzle eventually. I also have taken into consideration that half of
    * all possible configurations arent solvable by rearranging a solved 
    * puzzle.
 *****************************************************************************/
 
#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
# include <ctype.h>
#include <string.h>

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// board
int board[DIM_MAX][DIM_MAX];

// dimensions
int d;

// position blank tile, these are global variables because we want to 
// remember the positions during the whole game
int blank_tile_position_row;
int blank_tile_position_column;

// position blank tile for God mode, remembers positions during God-Mode.
// I also could have used the variables above of course...
int blank_row;
int blank_column;

// this variable keeps track how long the configuration list is, e.g. printing
// the amount of steps it took to solve the puzzle or for animation purposes
int index_configurations;

// GOD-mode was only intended to solve no more bigger than a 4x4 matrix
int configurations[4*4*4][4][4];

// prototypes, a.k.a. declaring functions
void clear(void);
void greet(void);
void init(int d); // could have used void here because 'd' is global, also I shouldnt comment like this
void draw(int d);
bool move(int tile);
bool won(void);

// functions for GOD-mode
bool function_God_Mode(void);
bool recursive(int index, int diepte);
bool move_blank(int move_direction);
void undo_move(int move_direction);
void animate_steps();

int main(int argc, string argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid dimensions
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init(d);

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw(d);

        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        string tile_input_string = GetString();
        
        // if user types in GOD.. start GOD-mode
        if (strcmp(tile_input_string, "GOD") == 0) {
            printf("solving by iterative deepening.. \n");
        
            if (function_God_Mode()) {
                
                printf("Get ready for the animation.. \n");
                usleep(5000000);
                // call function to animate steps GOD-mode took
                animate_steps();
                
                printf("God-mode solved the puzzle in %i steps"
                ".\n", index_configurations);
                break;
            }
            
        }
        else {
            int tile = atoi(tile_input_string);
            
            // move if possible, else report illegality
            if (!move(tile))
            {
                printf("\nIllegal move.\n");
                usleep(500000);
            }
        }
        
        // sleep thread for animation's sake
        usleep(5000);
    }
    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(200000);
}

/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).  
 */
void init(int d)
{
    // the board has to be filled in increasing order, such that it can be
    // random shuffled later
    int numbers = 1;

    // first for loop iterates through the rows
    for (int row = 0; row < d; row++) {
        
        // second for loop iterates through columns
        for (int column = 0; column < d; column++) {
            board[row][column] = numbers;
            numbers++;
        }
    }
    
    // final tile has to be 0 and not d*d
    board[d - 1][d - 1] = 0;
    
    // remember already blank tiles position into global variable
    blank_tile_position_row = d - 1;
    blank_tile_position_column = d - 1;
    
    // with drand48 we generate a random tile number, with the function move
    // (I made function move before this random shuffle) the program determines
    // if move is valid

    // you have to do this otherwise the numbers wouldnt be that random
    srand48((long int) time(NULL));
    
    // minimal 5 random swaps with maximum of 15 (otherwise it would take to 
    // long for the algorithm to solve the puzzle..)
    int random_steps = (int) ((drand48() * 10) + 5);
    int random_number_previous = 0;
    int number_of_swaps = 0;
    while (number_of_swaps < random_steps) {
        
        // generate random number between 1 till (d*d -1)
        int random_number = (int) ((drand48() * (d*d - 1)) + 1);
        
        // in case it would swap again with the same tile in a previous step
        if (random_number_previous != random_number) {
            if (move(random_number)){
                number_of_swaps++;
                random_number_previous = random_number;
            }
        }
            
    }
}

/**
 * Prints the board in its current state.
 */
void draw(int d)
{
    // same structure as in init - function, one loop iterates through rows,
    // other one iterates through columns
    for (int row = 0; row < d; row++) {
        for (int column = 0; column < d; column++) {
            
            // first check if the tile isn't 0
            if (board[row][column] != 0) {
                printf("%2d ", board[row][column]);
            }
            // because the tile with 0 is associated with an underscore
            else {
                printf(" _ ");
            }                
        }
        // for every row prints next line
        printf("\n");
    }
}

/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false. 
 */
bool move(int tile)
{
    // a boolean to check whether the tile can be swapped with the blank tile
    bool valid_swap = false;
    
    // variables for the position of the tile of the user input
    int position_row;
    int position_column;
    
    for (int row = 0; row < d; row++) {
        for (int column = 0; column < d; column++) {
            
            // if tile is found, save the positions
            if (board[row][column] == tile) {
                position_row = row;
                position_column = column;
            }
        }
    }
    
    // calculate how many rows and columns the tile of the user input is 
    // apart from the blank tile
    int diff_column = position_column - blank_tile_position_column;
    int diff_row = position_row - blank_tile_position_row;
    
    // first condition checks if the tile of user input is next to the blank
    // tile
    if (diff_column == 1 || diff_column == -1 || diff_row == 1 || 
        diff_row == -1) {
            
        // however, the tile of user also have to be adjecent (not diagonal)
        if (position_row == blank_tile_position_row || 
            position_column == blank_tile_position_column) {
                
            // if both conditions are met, then swap tile with blank tile
            board[blank_tile_position_row][blank_tile_position_column] = 
                                        board[position_row][position_column];
            board[position_row][position_column] = 0;
            
            // saving the new positions of the blank tile into global variables
            blank_tile_position_row = position_row;
            blank_tile_position_column = position_column;
            
            // swap succesfully means returning a boolean of true
            valid_swap = true;
        }
    }
    return valid_swap;
}

/**
 * Returns true if game is won (i.e., board is in winning configuration), 
 * else false.
 */
bool won(void)
{
    // only return true if the board reaches it's final state
    bool win_or_not_quite = false;
  
    // a counter to determine whether every tile is in right position
    int count_oplopend = 1;
    
    for (int row = 0; row < d; row++) {
        for (int column = 0; column < d; column++ ) {
            
            // the counter only adds +1 if the next tile in board has value of
            // 1 higher compared to previous tile
            if (board[row][column] == count_oplopend ) {
                count_oplopend = count_oplopend + 1;
            }
        }
    }
    
    // not only has count_ascending be equal to d*d, the last tile needs to be
    // the 0-tile
    if ((board[d - 1][d - 1] == 0) && count_oplopend == (d * d ) ) {
        win_or_not_quite = true;
    }
    
    return win_or_not_quite;
}

/**
 * Returns true if the game is solved. Furthermore, this function will call
 * a recursive function.
 */
bool function_God_Mode(void) {
    bool continue_different_function = false;
    
    // finding blank tile
    for (int row = 0; row < d; row++) {
        for (int column = 0; column < d; column++) {
            if (board[row][column] == 0) {
                blank_row = row;
                blank_column = column;
            }
        }
    } 
    
    // zero element in configuration array is the initial board when user
    // decides for playing God - mode
    for (int row = 0; row < d; row++) {
        for (int column = 0; column < d; column++) {
            int nummer = board[row][column];
            configurations[0][row][column] = nummer;
        }
    }

    // according to a paper of Ian Parberry the minimal number of moves to 
    // solve the n*n puzzle is in n^3 steps. n is d in this case
    int minimal_moves = d*d*d;
    for (int i = 1; i < minimal_moves; i++) {
    
        if (recursive(1, i)) {
            continue_different_function = true;
            
            // save this into global variable for animation purposes
            index_configurations = i + 1;
            break;
        } 
    
    }
    return continue_different_function;
}

// global variable needed to return true if puzzle is solved
bool doorgaan_andere_functie = false;

/**
 * Recursive function to determine the least amount of steps.
 */
bool recursive(int index, int diepte) { 
    
    // iterates from 0 to 4, these numbers represent the movement of blank tile
    for (int i = 0; i < 4; i++) {
        
        // determine whether the move of blank tile is valid and prevent
        // the function goes into this block of function when puzzle is already
        // solved
        if (move_blank(i)  && doorgaan_andere_functie == false) {
            
           
            // filling in the configuration of the puzzle in the array:
            // configurations
            for (int row = 0; row < d; row++) {
                for (int column = 0; column < d; column++) {
                    int nummer = board[row][column];
                    configurations[index][row][column] = nummer;
                }
            }
        
            // if this condition is met, you need to check whether the last
            // configuration is the solved one
            if (index == diepte) {
                
                // if so, break this function
                if (won()) {
                    printf("Final state of board: \n");
                    draw(d);
                    
                    doorgaan_andere_functie = true;
                    break;
                }
            }
            // else move again with the blank tile
            else {
                recursive(index + 1 , diepte);
            }
        
            // you need to undo a move after all moves are done
            undo_move(i);
            
        }
    }
    return doorgaan_andere_functie;
}

/**
 * Moving the blank tile.
 */
bool move_blank(int move_direction) { 
    bool continue_move = false;
    
    switch(move_direction) {
        
        case 0:
            // move blank up
            if (blank_row > 0) {
                board[blank_row][blank_column] = 
                                            board[blank_row - 1][blank_column]; 
                board[blank_row - 1][blank_column] = 0;
                blank_row = blank_row - 1;
                continue_move = true;
            }
            break;
            
        case 1:
            // move blank left
            if (blank_column > 0) {
                board[blank_row][blank_column] = 
                                            board[blank_row][blank_column - 1]; 
                board[blank_row][blank_column - 1] = 0;
                blank_column = blank_column - 1;
                continue_move = true;
            }
            break;
        case 2:
            // move blank down
            if ((blank_row) < (d - 1)) {
                board[blank_row][blank_column] = 
                                            board[blank_row + 1][blank_column];
                board[blank_row + 1][blank_column] = 0;
                blank_row = blank_row + 1;
                continue_move = true;
            }
            break;
        case 3:
            // move blank right
            if ( (blank_column) < (d -1) ) {
                board[blank_row][blank_column] = 
                                            board[blank_row][blank_column + 1];
                board[blank_row][blank_column + 1] = 0;
                blank_column = blank_column + 1;
                continue_move = true;
            }
            break;
    }
    
    return continue_move;
}

/**
 * Undo the move if only the above function was called first.
 */
void undo_move(int move_direction) {
    
    switch(move_direction) {
        
        case 0:
            // move blank down
            if ( (blank_row) < (d -1)) {
                board[blank_row][blank_column] = 
                                            board[blank_row + 1][blank_column];
                board[blank_row + 1][blank_column] = 0;
                blank_row = blank_row + 1;
            }
            break;
        case 1:
            // move blank right
            if ( (blank_column) < (d -1) ) {
                board[blank_row][blank_column] = 
                                            board[blank_row][blank_column + 1];
                board[blank_row][blank_column + 1] = 0;
                blank_column = blank_column + 1;
            }
            break;
        case 2:
            // move blank up
            if (blank_row > 0) {
                board[blank_row][blank_column] = 
                                            board[blank_row - 1][blank_column]; 
                board[blank_row - 1][blank_column] = 0;
                blank_row = blank_row - 1;
            }
            break;
        case 3:
            // move blank left
            if (blank_column > 0) {
                board[blank_row][blank_column] = 
                                            board[blank_row][blank_column - 1]; 
                board[blank_row][blank_column - 1] = 0;
                blank_column = blank_column - 1;
            }
            break;
    }
}
/**
 * Animate the steps.
 */
void animate_steps(void) {
    
    // just iterate through configurations and print each configuration of 
    // the puzzle
    for (int i = 0; i < index_configurations; i++) {
        for (int row = 0; row < d; row++) {
            for (int column = 0; column < d; column++){
                if (configurations[i][row][column] != 0) {
                    printf("%2d ", configurations[i][row][column]);
                }
                else {
                    printf(" _ ");
                }
            }
            printf("\n");
        }
        printf("\n");
        
        // for a smooth animation..
        usleep(1000000);
        
        // clear-function was already made by cs50, comes in handy for animating
        clear();
    }
} 

/**
 * Below I have commented al the code. Below is the code I tried
 * according to an algorithm from Ian Parberry. I have spent a whole day to 
 * implement this into God Mode. Unfortunately I didn't succeed with this
 * algorithm.
 */
/*
//bool space_up();
//bool space_down();
//bool space_left();
//bool space_right();
//void align();
//bool define_path(int move_space_left_or_right, int move_space_up_or_down);

//bool move_diagonal(int tile);
//bool move_vertical();

void align(int tile) {
    
    // finding blank tile
    for (int row = 0; row < d; row++) {
        for (int column = 0; column < d; column++) {
            if (board[row][column] == 0) {
                blank_row = row;
                blank_column = column;
            }
        }
    }
    
    // finding first tile to move to target position
    int tile_row;
    int tile_column;
    
    for (int row = 0; row <d;row++) {
        for (int column = 0; column < d; column++) {
            if (board[row][column] == tile) {
                tile_row = row;
                tile_column = column;
            }
        }
    }
    
    int move_space_left_or_right;
    int move_space_up_or_down;
    
    // move blank space right next to target tile
    if ( (tile_column) < (d - 1) ) {
        int right_of_target_row = tile_row;
        int right_of_target_column = tile_column + 1;
        
        int difference_row = right_of_target_row - blank_row;
        int difference_column =  right_of_target_column - blank_column;
        
        if (right_of_target_column == blank_column) {
            move_space_left_or_right = 0;
        }
        else {
            move_space_left_or_right = difference_column;
        }
        
        if (right_of_target_row == blank_row) {
            move_space_up_or_down = 0;
        }
        else {
            move_space_up_or_down = difference_row;
        }
        
    }
    
    else {
        int left_of_target_row = tile_row;
        int left_of_target_column = tile_column - 1;
        
        int difference_row = left_of_target_row - blank_row;
        int difference_column =  left_of_target_column - blank_column;
        
        if (left_of_target_column == blank_column) {
            move_space_left_or_right = 0;
        }
        else {
            move_space_left_or_right = difference_column;
        }
        if (left_of_target_row == blank_row) {
            move_space_up_or_down = 0;
        }
        else {
            move_space_up_or_down = difference_row;
        }
        
    } 
    if (define_path(move_space_left_or_right, move_space_up_or_down) ) {
        //move_diagonal(tile);
        draw(d);
    }
    return;
}

bool define_path(int move_space_left_or_right, int move_space_up_or_down) {
    
    if ( (move_space_left_or_right > 0 && move_space_up_or_down > 0) || 
    (move_space_left_or_right == 0 && move_space_up_or_down > 0) || 
    (move_space_left_or_right > 0 && move_space_up_or_down == 0) ){
        
        if ( space_right(move_space_left_or_right) ) {
            space_down(move_space_up_or_down);
        }
        else {
            space_down(move_space_up_or_down);
            space_right(move_space_left_or_right);
        }
    }
    else if ( (move_space_left_or_right > 0 && move_space_up_or_down < 0) || 
     (move_space_left_or_right == 0 && move_space_up_or_down < 0) ) {
        
        if (space_right(abs(move_space_left_or_right)) ) {
            space_up(abs(move_space_up_or_down));
        }
        else {
            space_up(abs(move_space_up_or_down));
            space_right(abs(move_space_left_or_right));
        }
    }
    else if ( (move_space_left_or_right < 0 && move_space_up_or_down > 0) || 
    (move_space_left_or_right < 0 && move_space_up_or_down == 0)) {
        if ( space_left( abs(move_space_left_or_right) ) ) {
            space_down(abs(move_space_up_or_down));
        }
        else {
            space_down(abs(move_space_up_or_down));
            space_left( abs(move_space_left_or_right));
        }
    }
    //else if (move_space_left_or_right <= 0 && move_space_up_or_down <= 0) {
    else {
        if ( space_left( abs(move_space_left_or_right) ) ) {
            space_up(abs(move_space_up_or_down));
        }
        else {
            space_up(abs(move_space_up_or_down));
            space_left( abs(move_space_left_or_right));
        }
    }
    
    return true;
}

bool space_right(int move_space_right) {
    bool juiste_pad = true;
  
    for (int i = 0; i < move_space_right; i++) {
        if (board[blank_row][blank_column + 1] == 1){
            
            for (int j = 0; j < i; j ++) {
                board[blank_row][blank_column] = board[blank_row][blank_column - 1];
                board[blank_row][blank_column - 1] = 0;
                blank_column = blank_column - 1;
            }
            juiste_pad = false;
            break;
        }
        else {
            board[blank_row][blank_column] = board[blank_row][blank_column + 1];
            board[blank_row][blank_column + 1] = 0;
            blank_column = blank_column + 1;
        }
    }
    
    return juiste_pad;
}

bool space_down(int move_space_down) {
  
    for (int i = 0; i < move_space_down; i++) {
        
        board[blank_row][blank_column] = board[blank_row + 1][blank_column];
        board[blank_row + 1][blank_column] = 0;
        blank_row = blank_row + 1;
        
    }
    return true;
}

bool space_up(int move_space_up) {
    
    for (int i = 0; i < move_space_up; i++) {
         
        board[blank_row][blank_column] = board[blank_row - 1][blank_column];
        board[blank_row - 1][blank_column] = 0;
        blank_row = blank_row - 1;
        
    }
    return true;
}

bool space_left(int move_space_left) {
    bool juiste_pad = true;
    
    for (int i = 0; i < move_space_left; i++) {
        if (board[blank_row][blank_column - 1] == 1){
            
            for (int j = 0; j < i; j ++) {
                board[blank_row][blank_column] = board[blank_row][blank_column + 1];
                board[blank_row][blank_column + 1] = 0;
                blank_column = blank_column + 1;
            }
            juiste_pad = false;
            break;
        }
        else {
            board[blank_row][blank_column] = board[blank_row][blank_column - 1];
            board[blank_row][blank_column - 1] = 0;
            blank_column = blank_column - 1;
        }
    }
    return juiste_pad;
} */


/*bool move_diagonal(int tile) {
    bool next_tile = false;
    
    
    // finding first tile to move to target position
    int tile_row;
    int tile_column;
    
    for (int row = 0; row <d;row++) {
        for (int column = 0; column < d; column++) {
            if (board[row][column] == tile) {
                tile_row = row;
                tile_column = column;
            }
        }
    }
    // first check wheter blank is left or right of target tile
    // if left, then swap
    if (blank_column < tile_column) {
        board[blank_row][blank_column] = board[blank_row][blank_column + 1];
        board[blank_row][blank_column + 1] = 0;
    }
    
    tile_row_end_position = tile / d;
    tile_column_end_position = tile % d - 1;
    
    while ((tile_row_end_position != tile_row) || 
    (tile_column_end_position != tile_column)) {
        
        // move diagonal, after full 6 steps then save new tile_row and tile_column
        
        // first step, move blank one square up
        board[blank_row][blank_column] = board[blank_row - 1][blank_column];
        board[blank_row - 1][blank_column] = 0;
        blank_row = blank_row - 1;
        
        // second step, move blank to the left
        board[blank_row][blank_column] = board[blank_row][blank_column - 1];
        board[blank_row][blank_column - 1] = 0;
        blank_column = blank_column - 1;
        
        // third step, swap with the target tile
        board[blank_row][blank_column] = board[blank_row + 1][blank_column];
        board[blank_row + 1][blank_column] = 0;
        blank_row = blank_row + 1;
        tile_row = tile_row - 1;
        
        // fourth step, move blank one square to the left
        board[blank_row][blank_column] = board[blank_row][blank_column - 1];
        board[blank_row ][blank_column - 1] = 0;
        blank_column = blank_column - 1;
        
        // fifth step, move blank one up
        board[blank_row][bla nk_column] = board[blank_row - 1][blank_column];
        board[blank_row - 1][blank_column] = 0;
        blank_row = blank_row - 1;
        
        // sixth step, swap with target tile
        board[blank_row][blank_column] = board[blank_row][blank_column + 1];
        board[blank_row][blank_column + 1] = 0;
        blank_column = blank_column + 1;
        tile_column = tile_column - 1;
    }
    
    // checken of ie al positie zit anders bepalen of ie nog horizontaal
    // of verticaal moet
    
    if ( (tile_row_end_position == tile_row) && (tile_column_end_position == tile_column) ) {
        next_tile = true;
        
    }
    else if (tile_row == tile_row_end_position) {
        move_horizontal(tile);
        next_tile = true;
    }
    else {
        move_vertical(tile, tile_row, tile_column);
        next_tile = true;
    }
        
    return next_tile;
}


bool move_vertical(int tile, int tile_row, int tile_column) {
    
    int tile_row_tmp = tile_row;
    int tile_column_tmp = tile_column;
    
    while (tile_row_end_position != tile_row_tmp) {
        
        // first step, move blank one square up
        board[blank_row][blank_column] = board[blank_row - 1][blank_column];
        board[blank_row - 1][blank_column] = 0;
        blank_row = blank_row - 1;
        
        // second step, move blank to the left
        board[blank_row][blank_column] = board[blank_row][blank_column - 1];
        board[blank_row][blank_column - 1] = 0;
        blank_column = blank_column - 1;
        
        // third step, swap with the target tile
        board[blank_row][blank_column] = board[blank_row + 1][blank_column];
        board[blank_row + 1][blank_column] = 0;
        blank_row = blank_row + 1;
        tile_row = tile_row - 1;
        
        //fourth step, blank goes one square to the right
        board[blank_row][blank_column] = board[blank_row][blank_column + 1];
        board[blank_row][blank_column + 1] = 0;
        blank_column = blank_column + 1;
        
        // fifth step, blank goes one up
        board[blank_row][blank_column] = board[blank_row - 1][blank_column];
        board[blank_row - 1][blank_column] = 0;
        blank_row = blank_row - 1;
        
    }
    
    return false;
}

bool move_horizontal() {

    return false;
} */