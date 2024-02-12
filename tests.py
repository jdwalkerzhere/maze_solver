from main import Maze 
from tkinter import Canvas
import unittest


def disable_function(function):
    def no_op(*arg, **kwargs):
        print(f"{function.__name__} has been disabled")

    return no_op


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 5
        num_rows = 10
        w1 = Maze()
        w1.canvas = Canvas()
        w1.selected_algo = "Depth First"

        # Set columns and rows directly
        w1.columns = num_cols
        w1.rows = num_rows

        # Now you can call _create_cells safely
        w1._create_cells()

        self.assertEqual(len(w1.cells), num_cols)
        self.assertEqual(len(w1.cells[0]), num_rows)

    # Warning Time-Consuming Test: Remove Decorator Cautiously
    @disable_function
    def test_recursion_failure(self):
        win = Maze()
        win.canvas = Canvas()
        win.selected_algo = "Depth First"

        num_repeats = 5

        for ind in range(175, 178):
            success, fail = 0, 0
            for mult in range(num_repeats):
                win.columns = ind
                win.rows = ind
                try:
                    win._create_cells()
                    success += 1
                except RecursionError:
                    fail += 1
            print()
            print(f"Success Rate {ind}: {(success/num_repeats)*100}%")
            print(f"Fail Rate {ind}: {(fail/num_repeats)*100}%")


if __name__ == "__main__":
    unittest.main()
