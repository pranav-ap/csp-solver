from core import *
import numpy as np
import pytest


def test_add_duplicate_variable():
    csp = CSP()

    csp.add_variable('a', [1, 2, 3])

    with pytest.raises(ValueError):
        csp.add_variable('a', [1, 2, 3])


def test_backtracking():
    csp = CSP()

    # add variables

    csp.add_variable('a', [1, 2, 3])
    csp.add_variable('b', [1, 2, 3])
    csp.add_variable('c', [1, 2, 3])

    # add constraints

    csp.add_constraint(lambda a, b: a < b, ['a', 'b'])
    csp.add_constraint(lambda b, c: b < c, ['b', 'c'])
    csp.add_constraint(MinSumConstraint(5))

    # Solve

    solver = BacktrackingSolver(csp)
    solution = solver.solve()

    assert solution == {'a': 1, 'b': 2, 'c': 3}


def test_min_conflicts():
    csp = CSP()

    # add variables

    csp.add_variable('a', [1, 2, 3])
    csp.add_variable('b', [1, 2, 3])
    csp.add_variable('c', [1, 2, 3])

    # add constraints

    csp.add_constraint(lambda a, b: a < b, ['a', 'b'])
    csp.add_constraint(lambda b, c: b < c, ['b', 'c'])
    csp.add_constraint(MinSumConstraint(5))

    # Solve

    solver = MinConflictsSolver(csp, 6000)
    solution, isValid = solver.solve()

    # assert isValid

    if isValid:
        assert solution == {'a': 1, 'b': 2, 'c': 3}


def test_n_rooks():
    csp = CSP()
    size = 5

    # add variables

    names = set(range(size * size))
    csp.add_variables(names, [True, False])

    # add constraints

    csp.add_constraint(count_equal_to_constraint(size, True))

    # row constraints

    for row_start in range(0, size * size, size):
        row_names = set(range(row_start, row_start + size))
        csp.add_constraint(
            count_le_constraint(1, True), row_names)

    # column constraints

    for col_start in range(0, size):
        col_names = set(range(col_start, size * size, size))
        csp.add_constraint(
            count_le_constraint(1, True), col_names)

    # solve

    #solver = MinConflictsSolver(csp)
    solver = BacktrackingSolver(csp)
    solution, isValid = solver.solve()
    assert isValid


def test_n_queens():
    csp = CSP()

    size = 5
    board = np.arange(size * size).reshape(size, size)

    # add variables

    names = set(range(size * size))
    csp.add_variables(names, [True, False])

    # add constraints

    csp.add_constraint(count_equal_to_constraint(size, True))

    # row constraints

    for row in board:
        csp.add_constraint(count_le_constraint(1, True), row)

    # column constraints

    for column in board.transpose():
        csp.add_constraint(count_le_constraint(1, True), column)

    # diagonal constraints

    diagonals = []

    diagonals.extend(board[::-1, :].diagonal(i)
                     for i in range(-board.shape[0] + 1, board.shape[1]))

    diagonals.extend(board.diagonal(i)
                     for i in range(board.shape[1] - 1, -board.shape[0], -1))

    for diagonal in diagonals:
        csp.add_constraint(count_le_constraint(1, True), diagonal)

    # solve

    solver = MinConflictsSolver(csp)
    #solver = BacktrackingSolver(csp)
    solution, isValid = solver.solve()
    print(solution, isValid)
    print('-----')

    for key, value in solution.items():
        if value:
            print(key)
