# Cops and Robbers

A research game designed to simulate biological systems. This game models a scenario where a "cop" and a "robber" move on a toroidal matrix, similar to chess kings or rooks, with the goal of determining the probability of capture under various conditions.

## Features

- **Toroidal Matrix**: The matrix wraps around like a torus, allowing movement through the walls.
- **Probabilistic Movement**: The cop and robber can move randomly with defined probabilities.
- **Turn-Based Simulation**: The game proceeds in a turn-based manner, with the robber moving first.
- **Customizable Parameters**: Adjust movement length, randomness, and other parameters to explore different scenarios.
- **Extended Functionality**: Future features include obstacles, additional agents, and more.

## Parameters

- `rob_drunk_pct` and `cop_drunk_pct`: Probability that the respective players move randomly.
- `rob_move_len` and `cop_move_len`: Number of moves allowed for the robber and cop per turn.
- `rob_loc` and `cop_loc`: Starting locations of the robber and cop.
- `diagonal_move`: Allows for diagonal movements.
- `pass_move`: Allows characters to skip their move.
- `multi_game`: Enables running multiple game simulations to calculate average results.
- `max_iter_per_game`: Maximum number of iterations per game.

## Usage

1. Clone the repository: `git clone https://github.com/YourUsername/CopsAndRobbers.git`
2. Navigate to the project directory.
3. Run the script: `python game.py`

## Play the Simulation

You can play the simulation online at: [Simulation Link](https://repl.it/@AaronLiftig/Cops-and-Robbers)
