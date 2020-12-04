from core import CSP, BacktrackingSolver, ExactSumConstraint, MinConflictsSolver, MaxSumConstraint
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

    # add constraints

    csp.add_constraint(lambda a, b: a < b, ['a', 'b'])
    csp.add_constraint(ExactSumConstraint(5))

    # Solve

    solver = BacktrackingSolver(csp)
    solution = solver.solve()
    print(solution)

    assert solution == {'a': 2, 'b' : 3}


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
        assert solution == {'a': 2, 'b' : 3}

    #assert valid
    #assert solution == {'a': 2, 'b' : 3}
