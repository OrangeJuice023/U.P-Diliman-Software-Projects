import itertools
import random as rand
from string import ascii_uppercase

# Constants
GRID_SIZE = 7
TOTAL_MINES = 8
COLUMNS = "ABCDEFG"

# Game state
class GameState:
    def __init__(self):
        self.mine_defuser_opened = False
        self.prompt_power_up = False
        self.used_power_up = False
        self.game_over = False

def generate_mines():
    """Generate 8 unique mine locations within a 7x7 grid"""
    return [
        ascii_uppercase[a] + str(b + 1) 
        for a, b in rand.sample(list(itertools.product(range(GRID_SIZE), repeat=2)), k=TOTAL_MINES)
    ]

def select_defuser(mines):
    """Select a defuser location and remove it from mines list"""
    defuser = rand.choice(mines)
    mines.remove(defuser)
    return defuser, mines

def set_cols(letter):
    """Map column letters to numerical indices"""
    column_map = {COLUMNS[i]: i for i in range(len(COLUMNS))}
    return column_map.get(letter)

def make_grid_game(mines, defuser):
    """Set up the initial grid with mines and the defuser"""
    grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Place defuser
    defuser_row = int(defuser[1]) - 1
    defuser_col = set_cols(defuser[0])
    grid[defuser_row][defuser_col] = "D"
    
    # Place mines
    for coord in mines:
        r = int(coord[1]) - 1
        c = set_cols(coord[0])
        grid[r][c] = "!"
    
    return grid

def count_surrounding_mines(grid):
    """Count surrounding mines for each cell in the grid"""
    rows, cols = len(grid), len(grid[0])
    cell_adj_dir = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
    
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols
    
    def count_adjacent_mines(x, y):
        count = 0
        for dx, dy in cell_adj_dir:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y) and grid[new_x][new_y] == "!":
                count += 1
        return count
    
    mine_counts = [["" for _ in range(cols)] for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "!":
                mine_counts[r][c] = "!"
            else:
                mine_counts[r][c] = count_adjacent_mines(r, c)
    
    return mine_counts

def game_look(display_grid, mines_left):
    """Display the current game state"""
    print("      A   B   C   D   E   F   G")
    
    for i, row in enumerate(display_grid, start=1):
        print("[{}]".format(i), end="   ")
        for cell in row:
            print("{}".format(cell), end="   ")
        print()
    
    print("\nThere are {} mines left.".format(mines_left))

def display_defuser_acquisition(state, defuser):
    """Display message when defuser is acquired"""
    if state.mine_defuser_opened and not state.prompt_power_up:
        print("\nNice! You got the defuse power-up at coordinate: {}!".format(defuser))
        state.prompt_power_up = True

def game_options(state):
    """Display available game options"""
    print("\nControls")
    print("Press [O] Open a cell")
    print("Press [F] Flag or unflag a cell")
    print("Press [E] Exit the game")
    if state.mine_defuser_opened and not state.used_power_up:
        print("Press [D] To use defuser")

def get_valid_coordinate():
    """Get and validate coordinate input from player"""
    received_coord = input("Hi Player, give me a coordinate ([A-G][1-7]): ").upper()
    
    if len(received_coord) == 2 and received_coord[0] in COLUMNS and received_coord[1] in "1234567":
        return int(received_coord[1]) - 1, set_cols(received_coord[0])
    else:
        print("Invalid coordinate: {}".format(received_coord))
        return None

def flood_fill_reveal(display_grid, actual_grid, reference_grid, r, c, state):
    """Recursively reveal cells starting from a zero-mine cell"""
    if r < 0 or r >= GRID_SIZE or c < 0 or c >= GRID_SIZE:
        return
    
    # Already revealed or flagged
    if display_grid[r][c] not in [".", "?"]:
        return
    
    # Don't auto-reveal flagged cells
    if display_grid[r][c] == "?":
        return
    
    # Check if it's the defuser
    if reference_grid[r][c] == "D":
        state.mine_defuser_opened = True
    
    # Reveal the cell
    display_grid[r][c] = actual_grid[r][c]
    
    # If it's a mine, stop (shouldn't happen in normal play)
    if actual_grid[r][c] == "!":
        return
    
    # If the cell has 0 adjacent mines, reveal all adjacent cells
    if actual_grid[r][c] == 0:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            flood_fill_reveal(display_grid, actual_grid, reference_grid, r + dr, c + dc, state)

def reveal_cell(display_grid, actual_grid, reference_grid, state):
    """Open a cell chosen by the player"""
    coord = get_valid_coordinate()
    if coord is None:
        return
    
    r, c = coord
    
    if display_grid[r][c] == "?":
        print("\nRemember, flagged cells cannot be opened unless unflagged.")
        return
    elif display_grid[r][c] == "*":
        print("\nLook, the mine is already defused.")
        return
    elif display_grid[r][c] != ".":
        # Cell already opened, try expansion mechanism
        expansion_mechanism(display_grid, actual_grid, reference_grid, r, c, state)
        return
    
    # Check if it's a mine
    if actual_grid[r][c] == "!":
        display_grid[r][c] = "!"
        return
    
    # Use flood fill to reveal cells
    flood_fill_reveal(display_grid, actual_grid, reference_grid, r, c, state)

def expansion_mechanism(display_grid, actual_grid, reference_grid, r, c, state):
    """Expand (chord) - reveal adjacent cells if flags match mine count"""
    cell_adj_dir = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    # Count adjacent flags and defused mines
    flag_count = 0
    for dr, dc in cell_adj_dir:
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < GRID_SIZE and 0 <= new_c < GRID_SIZE:
            if display_grid[new_r][new_c] in ["?", "*"]:
                flag_count += 1
    
    # If the number matches, reveal all unflagged adjacent cells
    if actual_grid[r][c] == flag_count:
        for dr, dc in cell_adj_dir:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < GRID_SIZE and 0 <= new_c < GRID_SIZE:
                if display_grid[new_r][new_c] == ".":
                    flood_fill_reveal(display_grid, actual_grid, reference_grid, new_r, new_c, state)
    else:
        print("\nHi player, a cell's number must match the count of surrounding flags or defused mines.")

def flag_cell(display_grid):
    """Flag or unflag a cell"""
    coord = get_valid_coordinate()
    if coord is None:
        return
    
    r, c = coord
    
    if display_grid[r][c] == ".":
        display_grid[r][c] = "?"
    elif display_grid[r][c] == "?":
        display_grid[r][c] = "."
    elif display_grid[r][c] == "*":
        print("\nYou are not allowed to flag a defused mine.")
    else:
        print("\nYou are not allowed to flag an already opened cell.")

def use_defuser(display_grid, actual_grid, reference_grid, state):
    """Use the defuser power-up"""
    coord = get_valid_coordinate()
    if coord is None:
        return
    
    r, c = coord
    
    # Mark as defused
    if reference_grid[r][c] == "!":
        display_grid[r][c] = "*"
        print("\nMine defused!")
    else:
        print("\nThis cell does not contain a mine, but it has been defused.")
    
    # Defuse adjacent cells
    cell_adj_dir = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dr, dc in cell_adj_dir:
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < GRID_SIZE and 0 <= new_c < GRID_SIZE:
            if actual_grid[new_r][new_c] == "!":
                display_grid[new_r][new_c] = "*"
            elif display_grid[new_r][new_c] == ".":
                flood_fill_reveal(display_grid, actual_grid, reference_grid, new_r, new_c, state)
    
    state.used_power_up = True

def count_flagged_cells(display_grid):
    """Count the number of flagged cells"""
    count = 0
    for row in display_grid:
        for cell in row:
            if cell in ["?", "*"]:
                count += 1
    return count

def mines_left_count(display_grid):
    """Calculate remaining mines based on flags"""
    total_mines = TOTAL_MINES - 1  # Minus the defuser
    flagged_count = count_flagged_cells(display_grid)
    mines_left = max(total_mines - flagged_count, 0)
    
    if mines_left == 0 and flagged_count > total_mines:
        print("Hi player, take note that flagged cells are now larger than mines.")
    
    return mines_left

def check_game_state(display_grid, actual_grid):
    """Check if the game is won or lost"""
    # Check for loss (revealed mine)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if display_grid[r][c] == "!" and actual_grid[r][c] == "!":
                return "loss"
    
    # Check for win (all non-mine cells revealed)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if actual_grid[r][c] != "!" and display_grid[r][c] in [".", "?"]:
                return "ongoing"
    
    return "win"

def handle_user_choice(display_grid, actual_grid, reference_grid, state):
    """Handle the user's menu choice"""
    choice = input("Enter choice: ").upper()
    
    if choice == "O":
        reveal_cell(display_grid, actual_grid, reference_grid, state)
    elif choice == "F":
        flag_cell(display_grid)
    elif choice == "D":
        if state.mine_defuser_opened and not state.used_power_up:
            use_defuser(display_grid, actual_grid, reference_grid, state)
        else:
            print("\nDefuser not available.")
    elif choice == "E":
        print("\nExiting Game! Goodbye Player.")
        return False
    else:
        print("\nInvalid choice. Please try again.")
    
    return True

def game_loop():
    """Main game loop"""
    # Initialize game
    mines = generate_mines()
    defuser, mines = select_defuser(mines)
    reference_grid = make_grid_game(mines, defuser)
    actual_grid = count_surrounding_mines(reference_grid)
    display_grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    state = GameState()
    
    print("Hello player, welcome to my minesweeper!\n")
    
    # Game loop
    while True:
        print()
        game_look(display_grid, mines_left_count(display_grid))
        
        # Check game state
        game_state = check_game_state(display_grid, actual_grid)
        if game_state == "loss":
            print()
            game_look(actual_grid, 0)
            print("\nYou stepped on a mine! Try again.")
            break
        elif game_state == "win":
            print()
            game_look(actual_grid, 0)
            print("\nCongratulations player! You win!")
            break
        
        # Display defuser acquisition if applicable
        display_defuser_acquisition(state, defuser)
        
        # Show options and get user choice
        game_options(state)
        if not handle_user_choice(display_grid, actual_grid, reference_grid, state):
            break

# Start the game
if __name__ == "__main__":
    game_loop()
