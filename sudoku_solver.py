from tkinter import Tk, Canvas, Entry, Button, END, Label


root = Tk()
root.title("Sudoku Solver")
root.resizable(False, False)
root.iconbitmap("icon.ico")

canvas = Canvas(root, width=450, height=500, bg="lightgrey")
canvas.pack()


# Constants for Sudoku grid values
GRID_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]


# Check for empty input (to allow deletion) or a single digit
def validate_input(new_text):
    if new_text == "" or (new_text.isdigit() and len(new_text) == 1):
        return True
    return False


# Class representing the GUI for a Sudoku tile.  Allow user to input values.
class Tile_GUI:
    def __init__(self, x, y, v, parent):
        self.x = x
        self.y = y
        self.v = v
        self.entry = Entry(
            parent,
            width=2,
            bd=0,
            font=("Arial", 24),
            justify="center",
            borderwidth=0,
            highlightthickness=0,
        )
        self.entry.place(x=x * 50 + 10, y=y * 50 + 60, width=35, height=35)
        self.vcmd = (root.register(validate_input), "%P")
        self.entry.config(validate="key", validatecommand=self.vcmd)


# Class representing a Sudoku tile
class Tile:
    def __init__(self, x, y, q, v):
        self.x = x
        self.y = y
        self.quadrant = q
        self.value = v


# Setup the initial grid
def setup_tiles():
    # Set each tile to have all possible values
    tiles = []
    for i in range(9):
        row = []
        for j in range(9):
            q = (i // 3) * 3 + (j // 3)
            row.append(Tile(i, j, q, GRID_VALUES.copy()))
        tiles.append(row)
    # Setup the graphical tiles
    gui = []
    for row in tiles:
        gui_row = []
        for tile in row:
            gui_row.append(Tile_GUI(tile.x, tile.y, 0, root))
        gui.append(gui_row)
    # Draw the outline for the quadrants
    canvas.create_line(0, 50, 450, 50, fill="black", width=4)
    canvas.create_line(0, 200, 450, 200, fill="black", width=4)
    canvas.create_line(0, 350, 450, 350, fill="black", width=4)
    canvas.create_line(0, 500, 450, 500, fill="black", width=4)
    canvas.create_line(3, 50, 3, 500, fill="black", width=4)
    canvas.create_line(150, 50, 150, 500, fill="black", width=4)
    canvas.create_line(300, 50, 300, 500, fill="black", width=4)
    canvas.create_line(450, 50, 450, 500, fill="black", width=4)

    return tiles, gui


# Helper to copy the grid
def copy_grid(tiles):
    return [[Tile(t.x, t.y, t.quadrant, t.value.copy()) for t in row] for row in tiles]


# Recursive backtracking solver
def solve(tiles):
    for x in range(9):
        for y in range(9):
            t = tiles[x][y]
            # If cell is not solved, try all possible values
            if len(t.value) != 1:
                for v in t.value:
                    # Make a deep copy of the grid
                    new_tiles = copy_grid(tiles)
                    # Assign the guess
                    new_tiles[x][y].value = [v]
                    # Propagate constraints
                    remove_values(new_tiles)
                    # Recursively attempt to solve
                    if solve(new_tiles):
                        # If solved, update original grid and return True
                        for i in range(9):
                            for j in range(9):
                                tiles[i][j].value = new_tiles[i][j].value
                        return True
                # If no value leads to a solution, backtrack
                return False
    # If all cells are solved, return True
    return True


# Get input values from the GUI
def get_starting_values(cell, gui):
    for y in range(9):
        for x in range(9):
            v = int(gui[x][y].entry.get() or 0)
            if v != 0:
                cell[x][y].value = [v]
    return cell


# Remove impossible values
def remove_values(tiles):
    for x in range(9):
        for y in range(9):
            t = tiles[x][y]
            if len(t.value) == 1:
                v = t.value[0]
                q = t.quadrant
                # Remove from row
                for j in range(9):
                    if j != y and v in tiles[x][j].value:
                        tiles[x][j].value.remove(v)
                # Remove from column
                for i in range(9):
                    if i != x and v in tiles[i][y].value:
                        tiles[i][y].value.remove(v)
                # Remove from quadrant
                for i in range(9):
                    for j in range(9):
                        other = tiles[i][j]
                        if other != t and other.quadrant == q and v in other.value:
                            other.value.remove(v)
    return tiles


# Solve the puzzle and update the graphical tiles
def solve_puzzle(cell, gui):
    cell = get_starting_values(cell, gui)
    if solve(cell):
        message_label.config(text="Solved!")
        for y in range(9):
            for x in range(9):
                value = cell[x][y].value[0]
                gui[x][y].entry.delete(0, END)
                gui[x][y].entry.insert(0, str(value))
    else:
        message_label.config(text="No solution found.")


# Clear the board and reset the GUI
def clear_board(cell, gui):
    for i in range(9):
        for j in range(9):
            cell[i][j].value = GRID_VALUES.copy()
            if gui[i][j].entry is not None:
                gui[i][j].entry.delete(0, END)
    message_label.config(text="")


cell, gui = setup_tiles()
# Setup the buttons and label placeholder
solve_button = Button(
    root, text="Solve", command=lambda: solve_puzzle(cell, gui), width=10
)
solve_button.place(x=40, y=10)
clear_button = Button(
    root, text="Clear", command=lambda: clear_board(cell, gui), width=10
)
clear_button.place(x=330, y=10)
message_label = Label(root, text="", bg="lightgrey", font=("Arial", 16))
message_label.place(relx=0.5, y=20, anchor="center")


root.mainloop()
