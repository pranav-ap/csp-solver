from core import *


def main():
    csp = CSP()
    size = 3

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
        col_names = set(range(col_start, col_start + size * 3, size))
        csp.add_constraint(
            count_le_constraint(1, True), col_names)

    # solve

    solver = MinConflictsSolver(csp)
    #solver = BacktrackingSolver(csp)
    solution, isValid = solver.solve()
    print(solution, isValid)


if __name__ == '__main__':
    main()
