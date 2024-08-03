# Arc Consistency


def revise(csp, X, Y):
    """
    - Revise the domain of X wrt domain of Y
    - Makes X arc consistent wrt Y
    """
    X_domain = csp.domains[X]
    Y_domain = csp.domains[Y]

    overlap = csp.get_overlap(X, Y)
    removals = []

    for X_tuple_value in X_domain:
        satisfied = False

        for Y_tuple_value in Y_domain:
            if csp.overlap_equality(X_tuple_value, Y_tuple_value, overlap):
                satisfied = True
                break

        if not satisfied:
            removals.append((X, X_tuple_value))

    is_revised = len(removals) > 0

    if is_revised:
        X_domain.difference_update(removals)

    return removals, is_revised


def arc_consistency(csp, queue) -> bool:
    queue = sorted(queue, key=lambda XY: len(csp.domains[XY[0]]), reverse=True)

    while queue:
        (X, Y) = queue.pop()
        removals, revised = revise(csp, X, Y)

        if revised:
            # no more values left in domain?
            if not len(csp.domains[X]):
                csp.restore(removals)
                return False

            other_neighbors = csp.neighbors[X].difference({Y})
            arcs = {(Z, X) for Z in other_neighbors if (Z, X) not in queue}
            queue.extend(arcs)

    return True


def AC3(csp) -> bool:
    queue = csp.get_edges()
    return arc_consistency(csp, queue)


def MAC(csp, name) -> bool:
    queue = csp.get_edges(of=name)
    return arc_consistency(csp, queue)
