from core.Constraint import ExactSumConstraint, MaxSumConstraint
from core import CSP, BacktrackingSolver, AllDifferentConstraint


def main():
    csp = CSP()

    # add variables

    csp.add_variable('a', [1, 2, 3])
    csp.add_variable('b', [2, 3])

    # add constraints

    csp.add_constraint(lambda a, b: a < b, ['a', 'b'])
    csp.add_constraint(ExactSumConstraint(5))

    # Solve

    solver = BacktrackingSolver(csp)
    solution = solver.solve()

    print(' - Solution -')
    print(solution)


if __name__ == '__main__':
    main()
