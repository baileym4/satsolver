"""
6.101 Lab 8:
SAT Solver
"""

#!/usr/bin/env python3

import sys
import typing

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS


def update_formula(formula, assignment):
    """
    updates the CNF formula as you go given an assignment
    assigment will be tuple: (object, bool)
    """
    # handle repeat rules
    new_formula = []

    item, bool_val = assignment
    if bool_val:
        opposite = False
    else:
        opposite = True
    # check each item

    for rule in formula:
        if assignment in rule:
            continue
        current_rule = rule.copy()
        while (item, opposite) in current_rule:
            current_rule.remove((item, opposite))
        new_formula.append(current_rule)

    return new_formula


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.
    """

    # for unit lengths
    formula.sort(key=len)
    # base cases
    if formula == []:
        return {}
    if formula is None:
        return None
    if formula[0] == []:
        return None

    ## recursive case

    current_assignment = formula[0][0]
    item = current_assignment[0]
    rest = update_formula(formula, (item, True))
    recursive_result_true = satisfying_assignment(rest)

    if recursive_result_true != None:
        recursive_result_true.update({item: True})
        return recursive_result_true

    # check False
    else:
        rest_f = update_formula(formula, (item, False))
        recursive_result_false = satisfying_assignment(rest_f)

        if recursive_result_false != None:
            recursive_result_false.update({item: False})
            return recursive_result_false


def row_helper(sudoku_board):
    """
    row is current row we are searching
    this recursively generates the constraints for a row in a sudoku board
    """

    # go through all squares
    # not more than one num per square
    # not less than one num per square
    row_formula = []
    dim = len(sudoku_board)
    for col in range(dim):
        for val in range(1, dim + 1):
            row_rule = []
            for row in range(dim):
                row_rule.append((((row, col), val), True))
                for subrow in range(row + 1, dim):
                    tup1 = (((row, col), val), False)
                    tup2 = (((subrow, col), val), False)
                    rule = [tup1, tup2]
                    row_formula.append(rule)
            row_formula.append(row_rule)
    return row_formula


def col_helper(sudoku_board):
    """
    returns CNF rules for columns
    """
    # make sure each square per column has at least one num
    # make sure it has at most one num
    col_formula = []
    dim = len(sudoku_board)
    for row in range(dim):
        for val in range(1, dim + 1):
            col_rule = []
            for col in range(dim):
                col_rule.append((((row, col), val), True))
                for subcol in range(col + 1, dim):
                    tup1 = (((row, col), val), False)
                    tup2 = (((row, subcol), val), False)
                    rule = [tup1, tup2]
                    col_formula.append(rule)
            col_formula.append(col_rule)
    return col_formula


def sub_grid_helper(sudoku_board):
    """
    gets rules for subgrids
    at most one coord in each max one coord in each
    """

    subgrid_formula = []
    dim = len(sudoku_board)
    subgrid_len = int(dim ** (1 / 2))

    for row in range(0, dim, subgrid_len):
        for col in range(0, dim, subgrid_len):
            coord = (row, col)
            subgrid_coords = find_subgrid_coords(coord, subgrid_len)
            for val in range(1, dim + 1):
                s_rule = []
                # make values for cnf formula
                for i, coord in enumerate(subgrid_coords):
                    s_rule.append(((coord, val), True))
                    if (i + 1) == len(subgrid_coords):
                        new_ind = 0
                    else:
                        new_ind = i + 1
                    next_coord = subgrid_coords[new_ind]
                    tup1 = ((coord, val), False)
                    tup2 = ((next_coord, val), False)
                    rule = [tup1, tup2]
                    subgrid_formula.append(rule)
                subgrid_formula.append(s_rule)
    return subgrid_formula


def find_subgrid_coords(coord, subgrid_len):
    """
    finds all coordinates within each subgrid
    """
    lower_row = coord[0]
    lower_col = coord[1]
    max_row = coord[0] + subgrid_len
    max_col = coord[1] + subgrid_len

    subgrid_coords = []

    for r in range(lower_row, max_row):
        for c in range(lower_col, max_col):
            subgrid_coords.append((r, c))

    return subgrid_coords


def intial_conditions_helper(sudoku_board):
    """
    create CNF formula based on intial conditions
    """
    # put initial conditions as rules
    # no more than one val in each square
    # no less than one val in each square

    initial_formula = []
    dim = len(sudoku_board)
    for r in range(dim):
        for c in range(dim):
            current_coord = sudoku_board[r][c]
            if current_coord != 0:
                initial_formula.append([(((r, c), current_coord), True)])
            rule = []
            for val in range(1, dim + 1):
                rule.append((((r, c), val), True))
                for subval in range(val + 1, dim + 1):
                    tup1 = (((r, c), val), False)
                    tup2 = (((r, c), subval), False)
                    rule_new = [tup1, tup2]
                    initial_formula.append(rule_new)
            initial_formula.append(rule)

    return initial_formula


def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    """
    sat_formula = []
    row_rules = row_helper(sudoku_board)
    col_rules = col_helper(sudoku_board)
    intial_rules = intial_conditions_helper(sudoku_board)
    subgrid_rules = sub_grid_helper(sudoku_board)

    # combine rules

    sat_formula.extend(row_rules)
    sat_formula.extend(col_rules)
    sat_formula.extend(intial_rules)
    sat_formula.extend(subgrid_rules)
    return sat_formula


def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolvable board, return None
    instead.
    """
    if assignments is None:
        return None
    return board_from_dict(assignments, n)


def board_from_dict(assignments, n):
    """
    given a dictionary of assignments create a sudoku board
    """

    assign_board = []
    row = [1] * n
    for _ in range(n):
        assign_board.append(row[:])

    # create dict with valid answers

    correct_assign = {}
    for spot in assignments:
        if assignments[spot]:
            correct_assign[spot[0]] = spot[1]
    print(correct_assign)
    print(len(correct_assign))
    for r in range(n):
        for c in range(n):
            if (r, c) in correct_assign:
                ans = correct_assign[(r, c)]
                assign_board[r][c] = ans

            else:
                assign_board[r][c] = 0
    return assign_board


if __name__ == "__main__":
    # formula = [
    # [('a', True), ('b', True), ('c', True)],
    # [('a', False), ('f', True)],
    # [('d', False), ('e', True), ('a', True), ('g', True)],
    # [('h', False), ('c', True), ('a', False), ('f', True)],
    # ]
    # new = update_formula(formula, ('a', True))
    # new_1 = update_formula(new, ('f', False))
    # ans = [[], [('h', False), ('c', True)]]
    # print(new_1)
    # if ans == new_1:
    #     print("yay")
    # else:
    #     print("no")
    # cnf = [
    #     [("a", True), ("b", True)],
    #     [("a", False), ("b", False), ("c", True)],
    #     [("b", True), ("c", True)],
    #     [("b", True), ("c", False)],
    #     [("a", False), ("b", False), ("c", False)],
    # ]
    # new_f = update_formula(cnf, ('a', True))
    # new_2 = update_formula(new_f, ('b', True))
    # print(new_2)
    # val = [[["a", True], ["a", False]], [["b", True], ["a", True]],[["b", True]],
    #        [["b", False],["b", False],["a", False]], [["c",True],["d",True]],
    #        [["c",True],["d",True]]]
    # output = satisfying_assignment(val)
    # print(output)
    # board_1 = [[1, 2, 3, 4], []]
    # ans = row_helper(board_1)
    # board_1 = [[1, 2, 0, 0], [0, 0, 0, 0], [0, 3, 0, 0], [0, 0, 4, 0]]
    # board_2 = [[1]]
    # ans1 = sudoku_board_to_sat_formula(board_2)
    # # print(ans1)

    # ans2 = row_helper(board_1)
    # print(ans2)

    # return arrays

    # bug ideas -- is the format of my cnf incorrect ?

    # combine helper functions
    # test sat_small_suduko_1
    small = [[1, 0, 0, 0], [0, 0, 0, 4], [3, 0, 0, 0], [0, 0, 0, 2]]
    formula = sudoku_board_to_sat_formula(small)
    # print(formula)
    # print(len(formula))
    assign = satisfying_assignment(formula)
    # print(assign)
    ans = assignments_to_sudoku_board(assign, 4)
    # print(ans)

    # this test should not be returning None but it is ---
    # this I think is an issue with my rules in the helper functions!!!
    # likley the same issue for all of my fails where None is not None

    # test case investigation for test_sat_sudoku_3
    board3 = [
        [0, 0, 1, 0, 0, 9, 0, 0, 3],
        [0, 8, 0, 0, 2, 0, 0, 9, 0],
        [9, 0, 0, 1, 0, 0, 8, 0, 0],
        [1, 0, 0, 5, 0, 0, 4, 0, 0],
        [0, 7, 0, 0, 3, 0, 0, 5, 0],
        [0, 0, 6, 0, 0, 4, 0, 0, 7],
        [0, 0, 8, 0, 0, 5, 0, 0, 6],
        [0, 3, 0, 0, 7, 0, 0, 4, 0],
        [2, 0, 0, 3, 0, 0, 9, 0, 0],
    ]
    # formula = sudoku_board_to_sat_formula(board3)
    # print(len(formula))
    # assign = satisfying_assignment(formula)
    # print(len(assign))
    # ans = assignments_to_sudoku_board(assign, 9)
