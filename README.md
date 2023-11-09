c# MineSweeper with a Twist

This is a Python implementation of the classic Minesweeper game. The codebase consists of several key functions and components to create and play the game.

## Key Functions and Components

Here's a brief overview of the key functions and components in the code:

- **generate_mines():** This function generates 8 unique mine locations within a 7x7 grid.

- **select_def(mines, defuser):** This function selects a defuser location and removes it from the list of generated mines.

- **set_cols(letter):** A function to map letters (columns) to numerical indices.

- **make_grid_game(mines, defuser):** Sets up the initial game grid with mines and the defuser.

- **count_surrounding_mines(grid):** Counts the surrounding mines for each cell in the grid.

- **game_look(display_unopened):** Displays the game's current state, including the grid and the number of mines left.

- **game_options():** Displays the available game controls and options for the player.

- **handle_user_choice():** Handles the player's input and game options.

- **reveal_chosen_cell(display_unopened, actual_grid, reference_of_grid):** Reveals a chosen cell and handles game logic.

- **expansion_mechanism(display_unopened, actual_grid, reference_of_grid, r, c):** Implements the expansion mechanism for the game.

- **get_valid_coordinate():** Prompts the player for a valid coordinate input.

- **flag_chosen_cell(display_unopened):** Allows the player to flag or unflag a cell.

- **use_power_up(display_unopened, actual_grid, reference_of_grid, grid):** Handles the use of the defuser power-up.

- **defuse_adjacent_mines(display_unopened, actual_grid, reference_of_grid, r, c):** Defuses adjacent mines when the defuser is used.

- **count_flagged_cells(display_unopened):** Counts the cells flagged as mines.

- **mines_initial(display_unopened):** Calculates the number of mines left based on flagged cells.

- **check_game_state(display_unopened, actual_grid):** Checks the game's state for a win, loss, or ongoing.

- **game_loop():** Executes the main game loop.

## Getting Started

### Prerequisites

You need to have Python installed on your system to run this game.

## Explanation per Function

**import itertools
import random as rand
from string import ascii_uppercase

# Created function to generate 8 unique mine locations within a 7x7 grid
def generate_mines():
    return [ascii_uppercase[a] + str(b + 1) for a, b in rand.sample(list(itertools.product(range(7), repeat=2)), k=8)]

# Function to select a defuser by technically removing it from the list of genererated mines
def select_def(mines, defuser):
    mines.remove(defuser)
    return mines**
