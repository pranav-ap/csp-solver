from core import *
import numpy as np


def main():
    csp = NaryCSP()

    # add variables

    csp.add_variable('a', {1, 2, 3})
    csp.add_variable('b', {1, 2, 3})
    csp.add_variable('c', {1, 2, 3})

    # add constraints

    csp.add_constraint(lambda a, b: a < b, ['a', 'b'])
    csp.add_constraint(lambda b, c: b < c, ['b', 'c'])
    # csp.add_constraint(min_sum_constraint(5))

    # Solve

    converter = DualCSPBuilder(csp)
    csp = converter.convert()
    print(csp)

    # solver = MinConflictsSolver(csp)
    # solver = BacktrackingSolver(csp)
    # solution, isValid = solver.solve()
    # print(solution, isValid)


if __name__ == '__main__':
    main()
