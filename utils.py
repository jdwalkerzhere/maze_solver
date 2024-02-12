from dataclasses import dataclass
from tkinter import Canvas


# Basic Utility for Drawing Line
@dataclass
class Point:
    x: int = 0
    y: int = 0


# Utility for Drawing on the Canvas
class Line:
    def __init__(self, p1: Point, p2: Point):
        self.point_one = p1
        self.point_two = p2

    # Utilizes Canvas create_line method to draw from p1 to p2
    def draw_line(self, canvas: Canvas, color: str):
        canvas.create_line(self.point_one.x,
                           self.point_one.y,
                           self.point_two.x,
                           self.point_two.y,
                           fill=color,
                           width=2)


# The Grid Cells to generate the Maze
class Cell:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bot_wall = True
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._canvas = canvas
        self.center_x = int((x1 + x2) / 2)
        self.center_y = int((y1 + y2) / 2)
        self.visited = False
        self.end = False

    # Method for drawing the cell onto the proper Canvas
    def draw_cell(self):
        # Helper Function for Coloring Walls Correctly
        def color(wall):
            return "black" if wall else "white"

        # Make the Four Corners of the Cell
        upper_left = Point(self._x1, self._y1)
        bottom_left = Point(self._x1, self._y2)
        upper_right = Point(self._x2, self._y1)
        bottom_right = Point(self._x2, self._y2)

        # Draw the Lines
        left_line = Line(upper_left, bottom_left)
        left_line.draw_line(self._canvas,
                            color(self.left_wall))
        bottom_line = Line(bottom_left, bottom_right)
        bottom_line.draw_line(self._canvas,
                              color(self.bot_wall))
        right_line = Line(bottom_right, upper_right)
        right_line.draw_line(self._canvas,
                             color(self.right_wall))
        top_line = Line(upper_left, upper_right)
        top_line.draw_line(self._canvas,
                           color(self.top_wall))

    # Method for drawing the path between two cells
    def draw_move(self, other_cell, undo=False):
        p1 = Point(self.center_x, self.center_y)
        p2 = Point(other_cell.center_x, other_cell.center_y)
        line = Line(p1, p2)
        line.draw_line(self._canvas, "red" if not undo else "gray")
