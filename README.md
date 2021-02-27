# CopsAndRobbers
## Combinatorics research game (for attempting to simulate biological systems)

A game of 'drunken' cops and robbers, where the cop and robber move similar to chess kings or rooks on an 0-indexed, mxn matrix that behaves like a torus. 

The goal is to find the probability of the cop capturing the robber under various conditions, including:
- Various sizes of a matrix, which the cop and robber traverse. The cop and robber can currently loop through the walls of the matrix, kind of like the game PacMan but all over the walls of the matrix. That is, the matrix acts like a torus.
- A probability representing how 'drunk' the robber and cop are, meaning how often they purposefully or randomly move.
- How many consecutive moves the robber and cop make per turn.

Currently, moves occur in a turn-based fashion, with the robber moving first. This avoids situations where the cop and robber cross paths but don't acknowledge each other. This turn-based nature may be modified in the future.

Multiple cycles of this game can be played in a row by changing the runTest option to True. The print statements have been made conditional on the runTest variable in order to have a manageable output.

Additional features will include spawning in new robbers and cops after certain conditions are met, ways for robbers to eliminate cops from the matrix, randomly placed obstacles on the matrix, etc.


## Parameters:

- **rob_drunk_pct** and **cop_drunk_pct** are the probability that the respective players move randomly

- **rob_move_len** and **cop_move_len** represent the number of moves the robber and cop are given each turn

- To manually place robber and cop, change **rob_loc** and/or **cop_loc** from 'random' a tuple representing one or both's placement on a 0-indexed, mxn matrix.

- **diagonal_move** allows for diagonal drunk movements

- **pass_move** allows for drunk characters to not move for their turn

- If you would like to calculate the average of a certain number of games, change **multi_game** to True and adjust the **num_of_games** accordingly. Print statments have been made conditional on the **multi_game** variable in order to have a manageable output screen.

- **max_iter_per_game** creates a max number of iterations per game
