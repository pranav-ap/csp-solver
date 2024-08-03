from core import *
import numpy as np
import pytest


def test_n_rooks():
    problem = Problem()
    size = 3

    # add variables

    names = set(range(size * size))
    problem.add_variables(names, [True, False])

    # add constraints

    problem.add_constraint(count_equal_to_constraint(size, True))

    # row constraints

    for row_start in range(0, size * size, size):
        row_names = set(range(row_start, row_start + size))
        problem.add_constraint(
            count_le_constraint(1, True), row_names)

    # column constraints

    for col_start in range(0, size):
        col_names = set(range(col_start, size * size, size))
        problem.add_constraint(
            count_le_constraint(1, True), col_names)

    # solve

    solver = BacktrackingSolver(problem)
    solution, isValid = solver.solve()
    assert isValid


def test_n_queens():
    problem = Problem()

    size = 3
    board = np.arange(size * size).reshape(size, size)

    # add variables

    names = set(range(size * size))
    problem.add_variables(names, [True, False])

    # add constraints

    problem.add_constraint(count_equal_to_constraint(size, True))

    # row constraints

    for row in board:
        problem.add_constraint(count_le_constraint(1, True), row)

    # column constraints

    for column in board.transpose():
        problem.add_constraint(count_le_constraint(1, True), column)

    # diagonal constraints

    diagonals = []

    diagonals.extend(board[::-1, :].diagonal(i)
                     for i in range(-board.shape[0] + 1, board.shape[1]))

    diagonals.extend(board.diagonal(i)
                     for i in range(board.shape[1] - 1, -board.shape[0], -1))

    for diagonal in diagonals:
        problem.add_constraint(count_le_constraint(1, True), diagonal)

    # solve

    solver = BacktrackingSolver(problem)
    solution, isValid = solver.solve()

    for key, value in solution.items():
        if value:
            print(key)


