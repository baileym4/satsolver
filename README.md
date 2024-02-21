# Sudoku Solver

This Python script is designed to solve Sudoku puzzles using the SAT (Boolean Satisfiability) problem-solving approach. It includes functions for updating the CNF (Conjunctive Normal Form) formula based on assignments, finding a satisfying assignment for a given CNF formula, and converting the assignment to a Sudoku board.

## Functionality

### `update_formula`

**Purpose:** Updates the CNF formula based on a given assignment.

**Usage:** `update_formula(formula, assignment)`

### `satisfying_assignment`

**Purpose:** Finds a satisfying assignment for a given CNF formula.

**Usage:** `satisfying_assignment(formula)`

### `row_helper`, `col_helper`, `sub_grid_helper`

**Purpose:** Generate CNF rules for rows, columns, and subgrids, respectively, in a Sudoku board.

**Usage:** `row_helper(sudoku_board)`, `col_helper(sudoku_board)`, `sub_grid_helper(sudoku_board)`

### `initial_conditions_helper`

**Purpose:** Create CNF rules based on initial conditions (pre-filled values) in a Sudoku board.

**Usage:** `initial_conditions_helper(sudoku_board)`

### `sudoku_board_to_sat_formula`

**Purpose:** Generates a SAT formula that represents a solution to the given Sudoku board.

**Usage:** `sudoku_board_to_sat_formula(sudoku_board)`

### `assignments_to_sudoku_board`

**Purpose:** Converts a satisfying assignment to a Sudoku board.

**Usage:** `assignments_to_sudoku_board(assignments, n)`

## Usage Example

```python
# Example Sudoku Board
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

# Convert Sudoku board to SAT formula
sat_formula = sudoku_board_to_sat_formula(sudoku_board)

# Find a satisfying assignment
assignment = satisfying_assignment(sat_formula)

# Convert the assignment to a Sudoku board
solved_board = assignments_to_sudoku_board(assignment, 9)

# Display the solved Sudoku board
print(solved_board)

## Testing
The test.py file contains test cases created by me and MIT 6.101 course staff. The server.py file can be run to play a sudoku game
