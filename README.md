# CopsAndRobbers
## Combinatorics research game

### A game of 'drunken' cops and robbers, where the cop and robber move similar to chess kings on an 0-indexed, mxn matrix. 

### The goal is to see the probability of the cop capturing the robber under various conditions, including:
#### Various sizes of a matrix, which the cop and robber traverse. The cop and robber can currently loop through the walls of the matrix, kind of like the game PacMan but all over the walls of the matrix. That is, the matrix acts like a sphere.
#### A probability representing how 'drunk' the robber and cop are, meaning how often they don't (forget) to move.
#### Whether the cop is chasing the robber or randomly moving, and whether the robber is avoiding the cop or randomly moving.
#### Whether the robber can make a 2-square move.

### Currently moves occur in a turn-based fashion, with the robber moving first. This avoids situations where the cop and robber cross paths but don't acknowledge each other. This turn-based nature may be modified in the future.

### Multiple cycles of this game can be played in a row by changing the runTest option to True.
