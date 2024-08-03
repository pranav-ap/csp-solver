from core import *
import pytest


def test_add_variables():
    problem = Problem()
    problem.add_variable("x", [0, 1])
    problem.add_variable("y", [0, 1])


def test_add_duplicate_variable():
    problem = Problem()
    problem.add_variable('a', [1, 2, 3])

    with pytest.raises(ValueError):
        problem.add_variable('a', [1, 2, 3])
