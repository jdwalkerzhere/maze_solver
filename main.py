from random import randint
from time import sleep
from tkinter import Canvas, Tk
from tkinter import ttk
from sys import setrecursionlimit
from utils import Cell, Line


"""
Note to Future Folk:

You'll note the `test_recursion_failure` method in tests.py.
I was noticing that *sometimes* the program would fail when
the nubmer of rows and columns would start exceeding 40 x 40.

Turns out that it begins failing at 42 x 42 (2% of the time),
and begins failing more than 30% of the time at 45 x 45.

I'm not sure where the recursion starts to break with the
new recusion limit set, but I'll probably set an upper bound
in the inputs section to make the normal experience consistent
"""
setrecursionlimit(10_000)


class Maze:
    # Our Algorithms for Users to Select from
    algos = ["Depth First",
             "Breadth First (TO BE BUILT)",
             "A* (TO BE BUILT)"]

    def __init__(self):
        # Setting up Window placement and Grid Configuration
        self.root = Tk()
        self.root.title("Maze Solver")
        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.scr_width, self.scr_height = self.screen_size()
        self.win_width = int(self.scr_height*0.75)
        self.win_height = self.win_width
        self.center_win()
        # self.root.resizable(width=False, height=False)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.error = None
        self.animate = False
        self.animation = []

        # Initialize Prompt Content
        self.prompt()

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    # Getting Screensize for Centering Window in Screen
    def screen_size(self):
        return self.root.winfo_screenwidth(), self.root.winfo_screenheight()

    # Centering Window in Screen
    def center_win(self):
        c_x = int((self.scr_width/2) - (self.win_width/2))
        c_y = int((self.scr_height/2) - (self.win_height/2))
        self.root.geometry(f"{self.win_width}x{self.win_height}+{c_x}+{c_y}")

    def draw_line(self, line: Line, color: str):
        line.draw_line(self.canvas, color)

    # Prompt Content
    def prompt(self):
        self.initial_content = ttk.Frame(self.root)
        self.initial_content.grid(column=0, row=0)

        self.col_row_lbl = ttk.Label(self.initial_content,
                                     text="Columns x Rows:")
        self.col_row_lbl.grid(column=0, row=0)
        self.col_row_entry = ttk.Entry(self.initial_content)
        self.col_row_entry.grid(column=1, row=0)

        self.algo_lbl = ttk.Label(self.initial_content, text="Which Algorithm")
        self.algo_lbl.grid(column=0, row=1)
        self.algo = ttk.Combobox(self.initial_content,
                                 values=self.algos,
                                 state="readonly")
        self.algo.grid(column=1, row=1)

        self.ani_lbl = ttk.Label(self.initial_content, text="Animate:")
        self.ani_lbl.grid(column=0, row=2)
        self.ani_input = ttk.Combobox(self.initial_content,
                                      values=["Yes", "No"],
                                      state="readonly")
        self.ani_input.grid(column=1, row=2)

        self.submit = ttk.Button(self.initial_content,
                                 text="Submit", command=self.validate_inputs)
        self.submit.grid(column=1, row=3)

    # On Submit Event, Validate inputs, and replace with Canvas
    def validate_inputs(self):
        # Validate Columns and Rows
        columns, rows = self.col_row_entry.get(), self.col_row_entry.get()
        try:
            columns, rows = int(columns), int(rows)
        except ValueError:
            self.error = ttk.Label(self.initial_content,
                                   text="Wrong type, Input Whole Number",
                                   foreground="red")
            self.error.grid(column=1, row=3)
            return

        # Removing Previous Error Message if it exists
        if self.error:
            self.error.destroy()

        # Validate Algorithm is selected
        self.selected_algo = self.algo.get()
        if not self.selected_algo:
            self.error = ttk.Label(self.initial_content,
                                   text="Please Select an Algorithm",
                                   foreground="red")
            self.error.grid(column=1, row=3)
            return

        # Set our Column & Row Members and destroy the input state
        self.columns, self.rows = columns, rows
        self.animate = True if self.ani_input.get() == "Yes" else False
        self.initial_content.destroy()
        self._create_cells()

    def _create_cells(self):
        self.canvas = Canvas(self.root, background="white")
        self.canvas.grid(column=0, row=0, sticky="nsew")

        # Get the step value based on # columns and # Rows
        self.cells = []

        w_inc = int(self.win_width / self.columns)
        h_inc = int(self.win_height / self.rows)

        for x in range(0, self.columns*w_inc, w_inc):
            inner_cells = []
            for y in range(0, self.rows*h_inc, h_inc):
                x1, y1 = x, y
                x2, y2 = x + w_inc, y + h_inc
                cell = Cell(self.canvas, x1, y1, x2, y2)
                self._draw_cell(cell)
                inner_cells.append(cell)
            self.cells.append(inner_cells)

        self._rm_walls_r()
        self._rm_walls()

    def _draw_cell(self, cell):
        cell.draw_cell()

    def _animate(self):
        self.redraw()
        sleep(0.00000001)  # Sleep for 1 microsecond

    # Removing Walls from Start and End Cells
    def _rm_walls(self):
        # Get Start and End Cells
        first_cell = self.cells[0][0]
        last_cell = self.cells[-1][-1]

        # Set Start Walls False
        first_cell.left_wall = False
        first_cell.bot_wall = False
        first_cell.right_wall = False
        first_cell.top_wall = False

        # Set End Walls False
        last_cell.left_wall = False
        last_cell.bot_wall = False
        last_cell.right_wall = False
        last_cell.top_wall = False

        # Setting Last Cell as End so we know!
        last_cell.end = True

        # Draw the White Cell Walls
        self._draw_cell(self.cells[0][0])
        self._draw_cell(self.cells[-1][-1])

        self._reset_visited()

    def _rm_walls_r(self, xp=0, yp=0):
        # Mark Current Cell as Visited
        self.cells[xp][yp].visited = True
        cellp = self.cells[xp][yp]

        while True:
            # Unvisited Cells to Go To
            to_visit = []
            # Left, Up, Right, Down
            adjacent = [(xp-1, yp),
                        (xp, yp-1),
                        (xp+1, yp),
                        (xp, yp+1)]

            # Confirm the Coordinates are in Bounds
            adjacent = [(x, y) for x, y in adjacent
                        if 0 <= x < self.columns
                        and 0 <= y < self.rows]

            # TODO: Add logic to avoid IndexError
            for x, y in adjacent:
                # Look Directly at Adjacent Cell
                cell = self.cells[x][y]

                # Add Unvisited Cells
                if not cell.visited:
                    to_visit.append((x, y))
            # Everything has been Visited, Exit
            if not to_visit:
                return

            # Pick Random from To_Visit
            xo, yo = to_visit[randint(0, len(to_visit)-1)]
            cello = self.cells[xo][yo]

            # Determine which wall to draw over
            if xo < xp and yo == yp:  # Left
                cellp.left_wall = False
                cello.right_wall = False
            elif xo == xp and yo < yp:  # Up
                cellp.top_wall = False
                cello.bot_wall = False
            elif xo > xp and yo == yp:  # Right
                cellp.right_wall = False
                cello.left_wall = False
            elif xo == xp and yo > yp:  # Down
                cellp.bot_wall = False
                cello.top_wall = False

            cellp.draw_cell()
            cello.draw_cell()

            self._rm_walls_r(xo, yo)

    def _reset_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

        self._solve()

    def _solve(self):
        match self.selected_algo:
            case "Depth First":
                self._depth_first()
                self._draw_it()
            case _:
                pass

    def _queue_it(self, c1, c2, undo):
        self.animation.append((c1, c2, undo))

    def _draw_it(self):
        for ind, values in enumerate(self.animation):
            if self.animate and ind % (self.columns // 10) == 0:
                self._animate()
            c1, c2, undo = values
            c1.draw_move(c2, undo)

    # TODO: Make Non-Recursive
    def _depth_first(self, x=0, y=0):
        # Mark Current Cell as Visited to Not Revisit
        current_cell = self.cells[x][y]
        current_cell.visited = True

        # If We've reached the End Exit
        if current_cell.end:
            return True

        # Getting Valid Directions for Searching
        directions = {"left":   (x-1, y),
                      "bottom": (x, y+1),
                      "right":  (x+1, y),
                      "top":    (x, y-1)}

        directions = {key: value for key, value
                      in directions.items()
                      if 0 <= value[0] < self.columns
                      and 0 <= value[1] < self.rows}

        for dir, (x, y) in directions.items():
            new_cell = self.cells[x][y]
            match dir:
                case "left":
                    if current_cell.left_wall or new_cell.visited:
                        continue
                    self._queue_it(current_cell, new_cell, False)
                    has_path = self._depth_first(x, y)
                    if has_path:
                        return True
                    self._queue_it(current_cell, new_cell, True)
                case "bottom":
                    if current_cell.bot_wall or new_cell.visited:
                        continue
                    self._queue_it(current_cell, new_cell, False)
                    has_path = self._depth_first(x, y)
                    if has_path:
                        return True
                    self._queue_it(current_cell, new_cell, True)
                case "right":
                    if current_cell.right_wall or new_cell.visited:
                        continue
                    self._queue_it(current_cell, new_cell, False)
                    has_path = self._depth_first(x, y)
                    if has_path:
                        return True
                    self._queue_it(current_cell, new_cell, True)
                case "top":
                    if current_cell.top_wall or new_cell.visited:
                        continue
                    self._queue_it(current_cell, new_cell, False)
                    has_path = self._depth_first(x, y)
                    if has_path:
                        return True
                    self._queue_it(current_cell, new_cell, True)

        return False


if __name__ == "__main__":
    window = Maze()
    window.wait_for_close()
