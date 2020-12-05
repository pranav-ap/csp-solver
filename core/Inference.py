from core.Variable import NameType
from .Constraint import Constraint
from .CSP import CSP


# Arc Consistency


def revise(csp: CSP, constraint: Constraint, x_name: NameType, y_name: NameType) -> bool:
    '''
    - Revise the domain of X wrt domain of Y
    - Makes X arc consistent wrt Y
    '''
    X = csp.domains[x_name]
    Y = csp.domains[y_name]

    revised_domain = [x for x in X for y in Y if constraint.is_satisfied(x, y)]
    is_revised = len(X) == len(revised_domain)

    if is_revised:
        csp.domains[x_name].replace(revised_domain)

    return is_revised


def arc_consistency(csp: CSP, binary_constraints) -> bool:
    while binary_constraints:
        constraint, [x, y] = binary_constraints.pop()

        if revise(csp, constraint, x, y):
            # no more values left in domain?
            if not csp.domains[x]:
                return False

            # add other related constraints
            related_constraints = csp.get_related_constraints(x, 2)
            filter(lambda cons, _: cons == constraint, related_constraints)
            binary_constraints.extend(related_constraints)

    return True


def AC3(csp: CSP) -> bool:
    binary_constraints = csp.get_constraints(2)
    return arc_consistency(csp, binary_constraints)


def MAC(csp: CSP, name: NameType) -> bool:
    binary_constraints = csp.get_related_constraints(name, 2)
    return arc_consistency(csp, binary_constraints)
