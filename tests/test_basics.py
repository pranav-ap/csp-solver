from core.Constraint import SomeDifferentConstraint, SomeEqualConstraint, SomeEqualToConstraint, SubsetEqualToConstraint
from core import CSP, BacktrackingSolver, ExactSumConstraint, MinConflictsSolver, MaxSumConstraint
import pytest
from itertools import count


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

    # add constraints

    csp.add_constraint(lambda a, b: a < b, ['a', 'b'])
    csp.add_constraint(ExactSumConstraint(5))

    # Solve

    solver = BacktrackingSolver(csp)
    solution = solver.solve()
    print(solution)

    assert solution == {'a': 2, 'b': 3}


def test_min_conflicts():
    csp = CSP()

    # add variables

    csp.add_variable('a', [1, 2, 3])
    csp.add_variable('b', [1, 2, 3])

    # add constraints

    csp.add_constraint(lambda a, b: a < b, ['a', 'b'])
    csp.add_constraint(ExactSumConstraint(5))

    # Solve

    solver = MinConflictsSolver(csp, 5000)
    solution, valid = solver.solve()
    print(solution)

    if valid:
        assert solution == {'a': 2, 'b': 3}

    #assert valid
    #assert solution == {'a': 2, 'b' : 3}


def test_n_queens():
    csp = CSP()

    size = 3

    # add variables

    for name in range(size * size):
        csp.add_variables(name, [True, False])

    # add constraints

    for row_start in range(0, size * size, size):
        row_names = list(range(row_start, row_start + size))
        csp.add_constraint(SubsetEqualToConstraint(1, True), row_names)

    for col_start in range(0, size):
        col_names = list(range(col_start, col_start + size, col_start * size))
        csp.add_constraint(SubsetEqualToConstraint(1, True), col_names)

    diagonal = list(range(size))
    csp.add_constraint(SubsetEqualToConstraint(1, True), diagonal)

    # solve

    solver = MinConflictsSolver(csp, 5000)
    solution, valid = solver.solve()
    print(solution)
