# Arc Consistency


def revise(csp, X, Y):
    '''
    - Revise the domain of X wrt domain of Y
    - Makes X arc consistent wrt Y
    '''
    X_domain = csp.curr_domains[X]
    Y_domain = csp.curr_domains[Y]

    revised = False
    removals = []

    for X_value in X_domain:
        conflict = True

        for Y_value in Y_domain:
            for constraint in csp.get_constraints_involving(X, {X, Y}):
                if constraint.is_satisfied({X: X_value, Y: Y_value}):
                    conflict = False
                    break

        if conflict:
            removed = csp.prune(X, X_value)
            removals.append(removed)
            revised = True

    return revised


def arc_consistency(csp, queue) -> bool:
    csp.support_pruning()
    sorted(queue, key=lambda XY: len(csp.curr_domains[XY[0]]), reverse=True)

    while queue:
        (X, Y) = queue.pop()

        if revise(csp, X, Y):
            # no more values left in domain?
            if not csp.curr_domains[X]:
                return False

            other_neighbors = csp.neighbors[X].difference({Y})
            queue.extend(other_neighbors)

    return True


def AC3(csp) -> bool:
    queue = {(X, Y)
             for X in csp.variables
             for Y in csp.neighbors[X]}

    return arc_consistency(csp, queue)


def MAC(csp, name) -> bool:
    queue = {(name, Y) for Y in csp.neighbors[name]}
    return arc_consistency(csp, queue)
