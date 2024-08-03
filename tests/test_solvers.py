from core import *
import pytest


def test_backtracking_no_constraints():
    problem = Problem()
    problem.add_variable("x", [0, 1])
    problem.add_variable("y", [0, 1])
    possible_solutions = [
        {"x": 0, "y": 0},
        {"x": 0, "y": 1},
        {"x": 1, "y": 0},
        {"x": 1, "y": 1},
    ]

    solver = BacktrackingSolver(problem)
    solution, isValid = solver.solve()

    assert isValid
    assert solution in possible_solutions


def make_problem():
    problem = Problem()

    # add variables

    problem.add_variable('a', [1, 2, 3])
    problem.add_variable('b', [1, 2, 3])
    problem.add_variable('c', [1, 2, 3])

    # add constraints

    problem.add_constraint(lambda a, b: a < b, ['a', 'b'])
    problem.add_constraint(lambda b, c: b < c, ['b', 'c'])
    problem.add_constraint(min_sum_constraint(5))

    return problem


def test_backtracking_with_constraints():
    problem = make_problem()

    solver = BacktrackingSolver(problem)
    solution, isValid = solver.solve()

    assert isValid
    assert solution == {'a': 1, 'b': 2, 'c': 3}


def test_min_conflicts_with_constraints():
    problem = make_problem()

    solver = MinConflictsSolver(problem, 6000)
    solution, isValid = solver.solve()

    if isValid:
        assert solution == {'a': 1, 'b': 2, 'c': 3}
