# 💣 MineSweeper with a Twist

A Python implementation of the classic Minesweeper game with a unique power-up mechanic! Find the hidden defuser to clear a 3x3 area of mines and gain a strategic advantage.

## 🎮 Game Features

- **7x7 Grid**: Compact game board with 7 mines
- **Defuser Power-Up**: Find the hidden defuser to clear a 3x3 area
- **Classic Mechanics**: Flag cells, chord/expand revealed numbers
- **Auto-Reveal**: Cells with 0 adjacent mines automatically expand
- **Intuitive Controls**: Simple keyboard-based interface

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed on your system

### Running the Game
```bash
python minesweeper.py
```

## 🎯 How to Play

### Game Objective
Reveal all safe cells without stepping on any mines. Use the defuser power-up strategically to clear dangerous areas!

### Controls
- **[O]** - Open a cell
- **[F]** - Flag/unflag a suspected mine
- **[D]** - Use defuser power-up (after finding it)
- **[E]** - Exit game

### Gameplay Tips
1. **Opening Cells**: Click on unopened cells to reveal them
   - Numbers indicate how many mines are adjacent (8-directional)
   - If you reveal a cell with 0 adjacent mines, surrounding cells auto-open
   
2. **Flagging**: Mark cells you believe contain mines with "?"
   - Helps track suspected mine locations
   - Affects the mine counter display

3. **Chording/Expansion**: Click on an already-opened number
   - If your adjacent flags equal the number, all unflagged neighbors open
   - Speeds up gameplay significantly

4. **Defuser Power-Up**: 
   - Hidden in one random cell (marked "D" internally)
   - When found, option [D] appears in the menu
   - Opens a 3x3 area, defusing all mines within
   - Use strategically on dangerous clusters!

### Grid Symbols
- `.` - Unopened cell
- `?` - Flagged cell (suspected mine)
- `*` - Defused mine
- `0-8` - Number of adjacent mines
- `!` - Mine (shown only when game ends)

## 📋 Code Structure

### Core Components

#### Game Initialization
- **`generate_mines()`**: Generates 8 unique mine locations within the 7x7 grid
  - Uses random sampling to ensure no duplicates
  - Returns coordinates in format like "A1", "B3", etc.

- **`select_defuser(mines)`**: Selects one mine location as the defuser power-up
  - Removes the selected location from the mines list
  - Returns both the defuser location and updated mines list

- **`make_grid_game(mines, defuser)`**: Creates the initial game grid
  - Places mines (!) and defuser (D) on the grid
  - Creates the reference grid used for game logic

#### Grid Processing
- **`set_cols(letter)`**: Maps column letters (A-G) to numerical indices (0-6)
  - Helper function for coordinate conversion

- **`count_surrounding_mines(grid)`**: Calculates adjacent mine counts
  - Processes each cell to count neighboring mines
  - Returns grid with numbers indicating danger levels

#### Display Functions
- **`game_look(display_grid, mines_left)`**: Displays the current game state
  - Shows the grid with proper formatting
  - Displays remaining mine count

- **`game_options(state)`**: Shows available controls
  - Dynamic menu based on game state
  - Shows defuser option when available

#### Game Mechanics
- **`reveal_cell(display_grid, actual_grid, reference_grid, state)`**: Opens a chosen cell
  - Validates the cell can be opened
  - Triggers flood fill for empty cells
  - Handles mine detonation

- **`flood_fill_reveal(display_grid, actual_grid, reference_grid, r, c, state)`**: Auto-reveals safe areas
  - Recursively opens cells with 0 adjacent mines
  - Classic Minesweeper behavior
  - Stops at numbered cells

- **`expansion_mechanism(display_grid, actual_grid, reference_grid, r, c, state)`**: Implements chording
  - Opens adjacent cells when flag count matches the cell number
  - Speeds up gameplay for experienced players

- **`flag_cell(display_grid)`**: Toggles flag status on a cell
  - Marks/unmarks suspected mines
  - Prevents accidental opening of flagged cells

#### Power-Up System
- **`use_defuser(display_grid, actual_grid, reference_grid, state)`**: Activates the defuser
  - Clears a 3x3 area around the selected coordinate
  - Marks defused mines with "*"
  - Auto-reveals safe adjacent cells
  - Can only be used once per game

- **`display_defuser_acquisition(state, defuser)`**: Notifies player when defuser is found
  - Displays message with defuser coordinate
  - Only shows once when first discovered

#### Helper Functions
- **`get_valid_coordinate()`**: Prompts and validates player input
  - Accepts format like "A1", "G7"
  - Returns row/column indices or None if invalid

- **`count_flagged_cells(display_grid)`**: Counts cells marked with flags or defused
  - Used for calculating remaining mines

- **`mines_left_count(display_grid)`**: Calculates mines remaining
  - Total mines minus flagged/defused cells
  - Displays warning if over-flagging occurs

#### Game State Management
- **`check_game_state(display_grid, actual_grid)`**: Determines win/loss/ongoing status
  - Checks if player revealed a mine (loss)
  - Checks if all safe cells are revealed (win)
  - Returns game status string

- **`GameState` class**: Manages game state variables
  - `mine_defuser_opened`: Whether defuser has been found
  - `prompt_power_up`: Whether defuser notification was shown
  - `used_power_up`: Whether defuser has been used
  - `game_over`: Whether game has ended

#### Main Loop
- **`game_loop()`**: Executes the main game cycle
  - Initializes game board and state
  - Handles user input and game flow
  - Checks win/loss conditions each turn
  - Displays appropriate end-game messages

### Constants
```python
GRID_SIZE = 7        # Board dimensions
TOTAL_MINES = 8      # Total mines generated (1 becomes defuser)
COLUMNS = "ABCDEFG"  # Column labels
```

## 🎲 Game Flow

1. **Initialization**
   - Generate 8 mine locations randomly
   - Select one mine as the defuser
   - Create grid with 7 active mines + 1 defuser
   - Initialize player display grid

2. **Game Loop**
   - Display current grid state
   - Show available controls
   - Process player input
   - Update grid based on action
   - Check win/loss conditions

3. **End Game**
   - Reveal entire grid
   - Display win/loss message
   - Exit or restart option

## 🐛 Bug Fixes from Original

This refactored version fixes several critical issues:

- ✅ Fixed duplicate nested loop in grid generation
- ✅ Fixed global variable scope issues with GameState class
- ✅ Implemented proper flood-fill algorithm
- ✅ Fixed defuser option not working in menu
- ✅ Corrected mine count calculation
- ✅ Removed duplicate/unused functions
- ✅ Improved expansion mechanism reliability

## 🤝 Contributing

Feel free to fork this project and submit pull requests for:
- Additional features (difficulty levels, larger grids, etc.)
- UI improvements
- Bug fixes
- Code optimizations

## 📝 License

This project is open source and available for educational purposes.

## 🎉 Enjoy the Game!

Challenge yourself to clear the board efficiently. Remember: the defuser is your secret weapon – use it wisely!

---

**Pro Tip**: Try to find the defuser early in the game for maximum strategic advantage!
