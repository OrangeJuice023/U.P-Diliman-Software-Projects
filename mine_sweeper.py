import itertools
import random as rand
from string import ascii_uppercase

# Created function to generate 8 unique mine locations within a 7x7 grid
def generate_mines():
    return [ascii_uppercase[a] + str(b + 1) for a, b in rand.sample(list(itertools.product(range(7), repeat=2)), k=8)]

# Function to select a defuser by technically removing it from the list of genererated mines
def select_def(mines, defuser):
    mines.remove(defuser)
    return mines

# Created functions to map the letters as columns to numerical indices
def set_cols(letter):
    column_letters = "ABCDEFG"
    column_map = {column_letters[i]: i for i in range(len(column_letters))}
    return column_map.get(letter)


# Joining the functionality of generate_mines() and select_def()
mines = generate_mines()
defuser = rand.choice(mines)
mines = select_def(mines, defuser)

# Created function to set up the initial grid with mines and the defuser
def make_grid_game(mines, defuser):
    grid = [["." for _ in range(7)] for _ in range(7)]

    defuser_row = int(defuser[1]) - 1
    defuser_col = set_cols(defuser[0])
    grid[defuser_row][defuser_col] = "D" # Put the defuser symbol in the grid

    for coord in mines:
  
      for coord in mines:
          if coord != defuser:
              r = int(coord[1]) - 1
              c = set_cols(coord[0])
              grid[r][c] = "!" # Put the mine symbol in the grid
  
      return grid

reference_of_grid = make_grid_game(mines, defuser)
grid = make_grid_game(mines, defuser)

# Created function to count surrounding mines for each cell in the grid
def count_surrounding_mines(grid):
    rows, cols = len(grid), len(grid[0])
    cell_adj_dir = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))

    # Created function counting adjacent mines and validating grid positions
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def count_adjacent_mines(x, y):
        count = 0
        for dx, dy in cell_adj_dir:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y) and grid[new_x][new_y] == "!":
                count += 1
        return count

    # Creates an empty mine count grid
    mine_counts = [["" for _ in range(cols)] for _ in range(rows)]

    # Calculate mine counts or mark mine locations
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "!":
                mine_counts[r][c] = "!"
            else:
                mine_counts[r][c] = count_adjacent_mines(r, c)

    return mine_counts


# Grid showing mine counts or mine locations
actual_grid = count_surrounding_mines(grid) 

# Initial display grid for the player
display_unopened = [["." for _ in range(7)] for _ in range(7)]

# Handles the look of the game
def game_look(display_unopened):
    # Display the game's initial state
    print("Hello player, welcome to my minesweeper! \n")
    print("      A   B   C   D   E   F   G")

    for i, row in enumerate(display_unopened, start=1):
        print("[{}]".format(i), end="   ")
        for cell in row:
            print("{}".format(cell), end="   ")
        print("")

    print("\nThere are {} mines left.".format(mines_initial(display_unopened)))

# Created function that enables the power-up scenario
def display_defuser_acquisition():
    global prompt_power_up
    if mine_defuser_opened and not prompt_power_up:
        print("\nNice! You got the defuse power-up at coordinate: {}!".format(str(defuser)))
        prompt_power_up = True

# Handles the look of the options for the player
def game_options():
    print("\nControls")
    print("Press [O] Open a cell")
    print("Press [F] flag or unflag a cell")
    print("Press [E] Exit the game")
    if mine_defuser_opened and not used_power_up:
        print("Press [D] To Use defuser")

# Handles the functionality of the game menu itself
def handle_user_choice():
    choice = input("Enter choice: ").upper()
    
    if len(choice) == 1:
        if choice == "O":
            received_coord = get_valid_coordinate()
            if received_coord is None:
                return True  # Return True to continue the game
            r, c = received_coord
            stack = [(r, c)]
            while stack:
                r, c = stack.pop()
                if display_unopened[r][c] == "?":
                    print("\nRemember, flagged cells cannot be opened unless unflagged.")
                elif display_unopened[r][c] == "*":
                    print("\nLook, the mine is already defused.")
                elif display_unopened[r][c] == ".":
                    if reference_of_grid[r][c] == "D":
                        display_unopened[r][c] = actual_grid[r][c]
                        mine_defuser_opened = True
                    else:
                        display_unopened[r][c] = actual_grid[r][c]
                else:
                    expansion_mechanism(display_unopened, actual_grid, reference_of_grid, r, c)
        elif choice == "F":
            flag_chosen_cell(display_unopened)
        elif choice == "E":
            print("\nExiting Game! Goodbye Player.")
            return False  # Return False to exit the game
    
    return True  # Return True to continue the game
    

def main_menu():
  # Check and display if the defuser power-up has been acquired but not prompted
  display_defuser_acquisition()

  # Display game controls and options for the player
  game_options()

  # Handle user choice and return a boolean indicating game continuation or stoppage
  return handle_user_choice()

# Created function that is responsible for the opening of the cell capability of the game
def reveal_chosen_cell(display_unopened, actual_grid, reference_of_grid):
  global mine_defuser_opened
  received_coord = get_valid_coordinate()
  if received_coord is None:
      print("\nInvalid coordinate. Please try again.")
      return main_menu()  # Return to the main menu if the coordinate is invalid

  r, c = received_coord
  stack = [(r, c)]

  while stack:
      r, c = stack.pop()
      if display_unopened[r][c] == "?":
          print("\nRemember, flagged cells cannot be opened unless unflagged.")
      elif display_unopened[r][c] == "*":
          print("\nLook, the mine is already defused.")
      elif display_unopened[r][c] == ".":
          if reference_of_grid[r][c] == "D":
              display_unopened[r][c] = actual_grid[r][c]
              mine_defuser_opened = True
          else:
              display_unopened[r][c] = actual_grid[r][c]
      else:
          expansion_mechanism(display_unopened, actual_grid, reference_of_grid, r, c)

# Executes the expansion mechanism for the minesweeper
def expansion_mechanism(display_unopened, actual_grid, reference_of_grid, r, c):
    cell_adj_dir = [
        (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]
    count = 0

    for dir in cell_adj_dir:
        new_r, new_c = r + dir[0], c + dir[1]
        if (
            0 <= new_r < len(display_unopened) and 0 <= new_c < len(display_unopened[0]) and
            (display_unopened[new_r][new_c] == "?" or display_unopened[new_r][new_c] == "*")
        ):
            count += 1

    if actual_grid[r][c] == count:
        for dir in cell_adj_dir:
            new_r, new_c = r + dir[0], c + dir[1]
            if 0 <= new_r < len(display_unopened) and 0 <= new_c < len(display_unopened[0]):
                if display_unopened[new_r][new_c] == "?" or display_unopened[new_r][new_c] == "*":
                    continue
                if reference_of_grid[new_r][new_c] == "D":
                    display_unopened[new_r][new_c] = actual_grid[new_r][new_c]
                    mine_defuser_opened = True
                display_unopened[new_r][new_c] = actual_grid[new_r][new_c]
    else:
        print("\nHi player, a cell's number must match the count of surrounding flags or defused mines.")


def get_valid_coordinate():
  while True:
      # Line responsible for requesting the player to input a coordinate (e.g., "A1", "B3", etc.)
      received_coord = input("Hi Player, give me a coordinate ([A-G][1-7]): ").upper()

      # Validate the input coordinate
      if len(received_coord) == 2 and received_coord[0] in "ABCDEFG" and received_coord[1] in "1234567":
          return int(received_coord[1]) - 1, set_cols(received_coord[0])
      else:
          # If the input format is incorrect or out of grid range, print an error message
          print("Invalid coordinate: {}".format(received_coord))
          return None  # Return None to indicate an invalid coordinate

# Allows user to flag a cell with a question mark
def flag_chosen_cell(display_unopened):
  input_coord = input("Hi Player, give me a coordinate ([A-G][1-7]): ").upper()

  if len(input_coord) == 2 and input_coord[0] in "ABCDEFG" and input_coord[1] in "1234567":
      r, c = int(input_coord[1]) - 1, set_cols(input_coord[0])

      if display_unopened[r][c] == ".":
         display_unopened[r][c] = "?"
         mines_initial(display_unopened)
      elif display_unopened[r][c] == "?":
          display_unopened[r][c] = "."
          mines_initial(display_unopened)
      elif display_unopened[r][c] == "*":
          print("\nYou are not allowed to flag a defused mine.")
      else:
          print("\nYou are not allowed to flag an already opened cell.")
  else:
      print("Invalid coordinate: {}".format(input_coord))
      return main_menu()  # Return to the main menu if the coordinate is invalid

# Created function for giving the defuse power-up a use
def use_power_up(display_unopened, actual_grid, reference_of_grid, grid):
  # Request the player to input a coordinate for using the defuser power-up
  input_coord = input("Hi Player, give me a coordinate ([A-G][1-7]): ").upper()

  # Line responsible to validate the input coordinate
  if len(input_coord) == 2 and input_coord[0] in "ABCDEFG" and input_coord[1] in "1234567":
      # If the input is a valid coordinate:
      # - Extract the row and column indices from the input
      r, c = int(input_coord[1]) - 1, set_cols(input_coord[0])

      # Check if the selected cell contains a mine ('!')
      if grid[r][c] == "!":
          # If the cell is a mine, defuse it by marking it with a '*'
          display_unopened[r][c] = "*"

          # Check adjacent cells for mines and defuse them
          defuse_adjacent_mines(display_unopened, actual_grid, reference_of_grid, r, c)
      else:
          # If the cell does not contain a mine, notify the player that it has been defused
          print("This cell does not contain a mine, but it has been defused.")

          # Check adjacent cells for mines and defuse them
          defuse_adjacent_mines(display_unopened, actual_grid, reference_of_grid, r, c)
  else:
      # If the input is not a valid coordinate, print an error message and return to the main menu
      print("Invalid coordinate: {}".format(input_coord))
      return main_menu()

# Instantiate variables that will be used for the defuser
mine_defuser_opened = False
prompt_power_up = False
used_power_up = False


def defuse_adjacent_mines(display_unopened, actual_grid, reference_of_grid, r, c):
  # Define directions to explore adjacent cells
  cell_adj_dir = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

  # Iterate through the adjacent cells
  for dir in cell_adj_dir:
      # Calculate the indices of adjacent cells based on current position (r, c)
      new_r, new_c = r + dir[0], c + dir[1]

      # Check if the calculated adjacent cell is within the grid boundaries
      if 0 <= new_r < len(display_unopened) and 0 <= new_c < len(display_unopened[0]):
          # Defuse the adjacent cells based on their content
          if actual_grid[new_r][new_c] == "!":
              display_unopened[new_r][new_c] = "*"
          else:
              display_unopened[new_r][new_c] = actual_grid[new_r][new_c]


# Checks number of mines left in the display grid based on the number of flags
def count_flagged_cells(display_unopened):
  count = 0

  # Iterates through each cell in the game grid
  for row in display_unopened:
      for cell in row:

          # Checks if the cell is flagged (marked as '?' or '*') and increments the count
          if cell in {"?", "*"}:
              count += 1
            
  return count

# Function to calculate mines left
def mines_initial(display_unopened):
  
  total_mines = 7 # Total number of mines in the game
  flagged_count = count_flagged_cells(display_unopened) # Count of cells flagged as mines

  # Calculate the number of mines yet to be identified
  mines_left_count = max(total_mines - flagged_count, 0)

  # Display a message if flagged cells exceed the total number of mines
  if mines_left_count == 0 and flagged_count > total_mines:
      print("Hi player, take note that flagged cells are now larger than mines.")

  return mines_left_count

# Function to check the game's state: win, loss, or ongoing
def check_game_state(display_unopened, actual_grid):
    for r in range(len(display_unopened)):
        for c in range(len(display_unopened[0])):
            if display_unopened[r][c] == "!":  # If any mine is revealed, it's a loss
                print("")
                game_look(actual_grid)
                print("\nYou stepped on a mine! Try again.")
                return True

    for r in range(len(display_unopened)):
        for c in range(len(display_unopened[0])):
            if (display_unopened[r][c] == "." or display_unopened[r][c] == "?") and actual_grid[r][c] != "!":
                return False  # If there are unopened cells that aren't mines, the game continues

    print("")
    game_look(actual_grid)
    print("\nCongratulations player! You win!")  # No unopened non-mine cells, it's a win
    return True

# Function to execute the game loop
def game_loop():
    while True:
        print("")
        game_look(display_unopened)
        if not main_menu():  # Check if the menu returned False (game stop)
            break
        if check_game_state(display_unopened, actual_grid):
            break

# Syntax to start the game loop
game_loop()
