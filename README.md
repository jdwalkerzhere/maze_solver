# Maze Solver

## Description

This Python project includes a graphical application that generates and solves mazes using various algorithms. Users can select an algorithm, specify maze dimensions, and watch the maze being solved in real time. The project demonstrates the use of recursion, algorithm implementation, and graphical user interface (GUI) creation with Tkinter.

## Installation

To run this project, you need Python 3.6 or later. Clone this repository to your local machine:

```bash
git clone https://yourrepositoryurl.com/maze-solver.git
cd maze-solver
```

No external dependencies are required as the project uses the standard Python library, including Tkinter for the GUI.

## Usage

To start the application, navigate to the project directory and run:

```bash
python main.py
```

Upon launching, the application will display a window where you can input the dimensions of the maze (columns x rows), select an algorithm from the dropdown menu, and choose whether to animate the maze solving process. After clicking "Submit", the maze generation will begin, followed by the solving process according to the selected algorithm.

### Example

- Enter `30` (or some other whole number) in the "Columns x Rows" field.
- Select "Depth First" from the "Which Algorithm" dropdown.
- Choose "Yes" for animation.
- Click "Submit" to start the maze generation and solving process.

## Testing

This project includes a basic testing suite to verify the functionality of maze generation and solving algorithms. To run the tests, execute:

```bash
python -m unittest tests.py
```

Note: The `test_recursion_failure` method is intentionally disabled to prevent time-consuming tests during normal test runs. Remove the `@disable_function` decorator to enable this test, keeping in mind it is designed for stress testing the recursion limits and may take a significant amount of time.

## Contributing

Contributions to the Maze Solver project are welcome. Please ensure to follow the project's coding standards and submit your pull requests for review.

## License

This project is open-source and available under the MIT License. See the LICENSE file for more details.
