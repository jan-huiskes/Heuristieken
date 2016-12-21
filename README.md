## Solving a rush hour board in python / Course: Heuristieken

### Using the command-line
To solve a desired board configuration with a specific algorithm one must use the command-line. For example: if you want to solve the first board (which is 6x6) with breadth first, then you have to fetch:

    python rush_hour.py breadth board1

to the command-line. Some more examples are as indicated:

#### A* algorithm
    python rush_hour.py astar board2

#### Iterative deepening
    python rush_hour.py id board3

#### Random
    python rush_hour.py random board7
    
You could also make use of the animation only. The animations are provided in the /Boards folder, which were in an earlier stage made.

#### Animate a board
    python rush_hour.py animation board1

The 12x12 board could also be animated. This board however is obtained by a random solver, whereas the other boards were solved by A*.
