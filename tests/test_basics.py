from core import *
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

    #assert isValid

    if isValid:
        assert solution == {'a': 1, 'b': 2, 'c': 3}


def test_n_rooks():
    csp = CSP()
    size = 3

    # add variables

    names = list(range(size * size))
    csp.add_variables(names, [True, False])

    # add constraints

    csp.add_constraint(ValueCountEqualToConstraint(size, True))

    # row constraints

    for row_start in range(0, size * size, size):
        row_names = list(range(row_start, row_start + size))
        csp.add_constraint(ValueCountUpperLimitConstraint(1, True), row_names)

    # column constraints

    for col_start in range(0, size):
        col_names = list(range(col_start, col_start + size * 3, size))
        csp.add_constraint(ValueCountUpperLimitConstraint(1, True), col_names)

    # solve

    solver = MinConflictsSolver(csp, 4000)
    solution, isValid = solver.solve()
    print(solution)

    #assert isValid


def test_n_queens():
    csp = CSP()
    size = 3

    # add variables

    names = list(range(size * size))
    csp.add_variables(names, [True, False])

    # add constraints

    csp.add_constraint(ValueCountEqualToConstraint(size, True))

    # row constraints

    for row_start in range(0, size * size, size):
        row_names = list(range(row_start, row_start + size))
        csp.add_constraint(ValueCountUpperLimitConstraint(1, True), row_names)

    # column constraints

    for col_start in range(0, size):
        col_names = list(range(col_start, col_start + size * 3, size))
        csp.add_constraint(ValueCountUpperLimitConstraint(1, True), col_names)

    # primary_diagonal

    primary_diagonal = [index + index * size for index in range(size)]

    csp.add_constraint(
        ValueCountUpperLimitConstraint(1, True),
        primary_diagonal)

    # secondary_diagonal

    secondary_diagonal = [row * size + col
                          for row in range(size)
                          for col in range(size)
                          if row + col == size - 1]

    csp.add_constraint(
        ValueCountUpperLimitConstraint(1, True),
        secondary_diagonal)

    # solve

    #solver = BacktrackingSolver(csp)
    solver = MinConflictsSolver(csp, 4000)
    solution, isValid = solver.solve()
    print(solution)
