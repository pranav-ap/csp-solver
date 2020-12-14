# Arc Consistency


def revise(csp, X, Y):
    '''
    - Revise the domain of X wrt domain of Y
    - Makes X arc consistent wrt Y
    '''
    X_domain = csp.domains[X]
    Y_domain = csp.domains[Y]
    removals = []

    binary_constraints = csp.get_constraints_involving(X, {X, Y})

    for constraint in binary_constraints:
        for X_value in X_domain:
            satisfied = False

            for Y_value in Y_domain:
                assignment = {X: X_value, Y: Y_value}

                if constraint.is_satisfied(assignment):
                    satisfied = True
                    break

            if not satisfied:
                removals.append((X, X_value))

    is_revised = len(removals) > 0

    if is_revised:
        X_domain.difference_update(removals)

    return removals, is_revised


def arc_consistency(csp, queue) -> bool:
    sorted(queue, key=lambda XY: len(csp.domains[XY[0]]), reverse=True)

    while queue:
        (X, Y) = queue.pop()

        removals, revised = revise(csp, X, Y)

        if revised:
            # no more values left in domain?
            if not len(csp.domains[X]):
                csp.restore(removals)
                return False

            other_neighbors = csp.neighbors[X].difference({Y})
            queue.update({(Z, X) for Z in other_neighbors})

    return True


def forward_checking(csp, X, assignment):
    removals = []

    # for Y in csp.neighbors[X].difference(assignment.keys()):
    #     binary_constraints = csp.get_constraints_involving(X, {X, Y})

    #     for constraint in binary_constraints:
    #         for Y_value in csp.domains[Y]:
    #             assignment = {**assignment, Y: Y_value}

    #             if not constraint.is_satisfied(assignment):
    #                 removals.append((Y, Y_value))

    # satisfied = len(removals) == 0

    return removals


def AC3(csp) -> bool:
    queue = {(X, Y)
             for X in csp.variables
             for Y in csp.neighbors[X]}

    return arc_consistency(csp, queue)


def MAC(csp, name) -> bool:
    queue = {(name, Y) for Y in csp.neighbors[name]}
    return arc_consistency(csp, queue)
