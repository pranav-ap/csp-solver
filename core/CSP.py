from .Constraint import Constraint


class CSP:
    def __init__(self) -> None:
        self.variables = set()  # just the names
        self.domains = {}  # name -> (values)
        self.constraints = []  # [Constraint]

        self.neighbors = {}  # name -> set(names)
        self.constraints_map = {}  # name -> set(Constraint)

    def add_variable(self, name, domain):  # domain is a set
        if name in self.variables:
            raise ValueError('${name} is already declared as a variable')

        self.variables.add(name)
        self.domains[name] = domain or set()
        self.neighbors[name] = set()
        self.constraints_map[name] = set()

    def add_variables(self, names, domain):
        for name in names:
            self.add_variable(name, domain)

    def add_constraint(self, constraint, params=None):  # scope is a list
        params = params or list(self.variables)
        scope = set(params)

        constraint = Constraint(constraint, scope, params)

        self.constraints.append(constraint)

        for name in scope:
            self.constraints_map[name].add(constraint)

        for name in scope:
            other_neighbors = scope.difference({name})
            self.neighbors[name].update(other_neighbors)

    def is_complete(self, assignment):
        keys = set(assignment.keys())
        return keys == self.variables

    def get_constraints_involving(self, name, scope):
        constraints = [constraint
                       for constraint in self.constraints_map[name]
                       if constraint.scope == scope]

        return constraints

    # Domain

    def restore(self, removals):
        for name, value in removals:
            self.domains[name].add(value)

    def suppose(self, name, value):
        removals = [(name, val) for val in self.domains[name] if val != value]
        self.domains[name] = {value}
        return removals

    # Assignment

    def assign(self, var, val, assignment):
        assignment[var] = val

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
