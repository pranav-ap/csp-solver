from .Constraint import Constraint
from copy import deepcopy


class CSP:
    def __init__(self) -> None:
        self.variables = set()  # just the names
        self.domains = {}  # name -> (values)
        self.constraints = []  # [Constraint]

        self.neighbors = {}  # name -> set(names)
        self.constraints_map = {}  # name -> set(Constraint)
        self.curr_domains = None

    def add_variable(self, name, domain):
        if name in self.variables:
            raise ValueError('${name} is already declared as a variable')

        self.variables.add(name)
        self.domains[name] = domain or []
        self.neighbors[name] = set()
        self.constraints_map[name] = set()

    def add_variables(self, names, domain):
        for name in names:
            self.add_variable(name, domain)

    def add_constraint(self, constraint, scope=None):
        scope = scope or self.variables
        constraint = Constraint(scope, constraint)

        self.constraints.append(constraint)

        # update constraint_map

        for name in scope:
            self.constraints_map[name].add(constraint)

        # update neighbors

        neighbors = {name: scope.difference({name}) for name in scope}

        for name, scope in neighbors.items():
            self.neighbors[name].update(scope)

    def is_consistent(self, assignment):
        return all(constraint.is_satisfied(assignment)
                   for constraint in self.constraints
                   if all(name in assignment for name in constraint.scope))

    def is_complete(self, assignment):
        keys = set(assignment.keys())
        return keys == self.variables

    def get_constraints_involving(self, name, scope):
        constraints = [constraint
                       for constraint in self.constraints_map[name]
                       if constraint.scope == scope]

        return constraints

    # Domain

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = deepcopy(self.domains)

    def prune(self, var, value):
        self.curr_domains[var].remove(value)
        return (var, value)

    def restore(self, removals):
        for name, value in removals:
            self.curr_domains[name].add(value)

    def choices(self, name):
        return (self.curr_domains or self.domains)[name]

    def suppose(self, name, value):
        self.support_pruning()
        removals = [(name, val)
                    for val in self.curr_domains[name] if val != value]
        self.curr_domains[name] = {value}
        return removals

    # Assignment

    def assign(self, var, val, assignment):
        assignment[var] = val

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
