from core.Constraint import ValueCountEqualToConstraint, ValueCountUpperLimitConstraint
from core.ConstraintSolver import BacktrackingSolver, MinConflictsSolver
from core import CSP


def main():
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

    solver = BacktrackingSolver(csp)
    solution = solver.solve()
    print(solution)


if __name__ == '__main__':
    main()
